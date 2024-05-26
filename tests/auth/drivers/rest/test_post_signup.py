import pytest
from faker import Faker
from fastapi import status

from tests.auth.builders.domain.entities.user_builder import UserBuilder
from tests.auth.builders.use_cases.inputs.create_user_input_builder import (
    CreateUserInputBuilder,
)
from tests.auth.helpers.auth_database_client import AuthDatabaseClient
from tests.auth.helpers.auth_http_client import AuthHttpClient
from tests.helpers.server_test import ServerTest


@pytest.mark.anyio(scope="class")
@pytest.mark.describe("POST /auth/signup")
class TestPostSignup:
    @pytest.mark.it(f"Should return {status.HTTP_200_OK} OK")
    async def test_signup_ok(self) -> None:
        async with ServerTest() as (http_client, pool):
            # given
            auth_client = AuthHttpClient(http_client)
            auth_database_client = AuthDatabaseClient(pool)

            # and
            body = CreateUserInputBuilder().build_dict()

            # when
            response = await auth_client.signup(body)

            # then
            assert response.status_code == status.HTTP_201_CREATED

            # and
            output = response.json()

            # and
            assert "id" in output
            user_id = output["id"]

            # and
            user = await auth_database_client.select_user(user_id)
            assert user

            # and
            fields = [
                "id",
                "email",
                "first_name",
                "last_name",
                "updated_at",
                "created_at",
            ]
            user_dict = user.model_dump(mode="json")
            for field in fields:
                assert field in output
                assert field in user_dict
                assert output[field] == user_dict[field]

            # and
            assert set(fields) == set(output.keys())

    @pytest.mark.it(f"Should return {status.HTTP_409_CONFLICT} CONFLICT")
    async def test_signup_email_in_use(self) -> None:
        async with ServerTest() as (http_client, pool):
            # given
            auth_client = AuthHttpClient(http_client)
            auth_database_client = AuthDatabaseClient(pool)

            # and
            user = UserBuilder().build()
            await auth_database_client.create_user(user)

            # and
            body = CreateUserInputBuilder().with_email(user.email).build_dict()

            # when
            response = await auth_client.signup(body)

            # then
            assert response.status_code == status.HTTP_409_CONFLICT

            # and
            output = response.json()
            assert output == {"detail": "Email already exists"}

    @pytest.mark.it(
        f"Should return {status.HTTP_422_UNPROCESSABLE_ENTITY} "
        "UNPROCESSABLE_ENTITY"
    )
    async def test_signup_invalid_password(self, faker: Faker) -> None:
        async with ServerTest() as (http_client, _):
            # given
            auth_client = AuthHttpClient(http_client)

            # and
            body = (
                CreateUserInputBuilder()
                .with_password(faker.password())
                .build_dict()
            )

            # when
            response = await auth_client.signup(body)

            # then
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

            # and
            output = response.json()
            assert "detail" in output
            assert len(output["detail"]) == 1
            assert "msg" in output["detail"][0]
            assert "passwords do not match" in output["detail"][0]["msg"]
