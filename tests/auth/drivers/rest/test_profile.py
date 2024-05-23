import secrets
from uuid import uuid4

import pytest
from faker import Faker
from fastapi import status

from tests.auth.builders.domain.entities.user_builder import UserBuilder
from tests.auth.helpers.auth_database_client import AuthDatabaseClient
from tests.auth.helpers.auth_http_client import AuthHttpClient
from tests.auth.helpers.generate_token import generate_token
from tests.helpers.server_test import ServerTest


@pytest.mark.anyio(scope="class")
@pytest.mark.describe("GET /auth/profile")
class TestProfile:
    @pytest.mark.it(f"Should return {status.HTTP_200_OK} OK")
    async def test_profile_ok(self, faker: Faker) -> None:
        secret_key = secrets.token_hex(64)
        env = {"SECRET_KEY": secret_key}
        async with ServerTest(env) as (http_client, pool):
            # given
            raw_password = faker.password()
            user = UserBuilder().with_hashed_password(raw_password).build()
            token = generate_token(user.id, secret_key=secret_key)

            # and
            auth_database_client = AuthDatabaseClient(pool)
            await auth_database_client.create_user(user)

            # and
            auth_client = AuthHttpClient(http_client)

            # when
            response = await auth_client.profile(token)

            # then
            assert response.status_code == status.HTTP_200_OK

            # and
            output = response.json()
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

    @pytest.mark.it(
        f"Should return {status.HTTP_401_UNAUTHORIZED} "
        "UNAUTHORIZED when token is not valid"
    )
    async def test_profile_unauthorized_token(self) -> None:
        async with ServerTest() as (http_client, _):
            # given
            secret_key = secrets.token_hex(64)
            user_id = uuid4()
            token = generate_token(user_id, secret_key=secret_key)

            # and
            auth_client = AuthHttpClient(http_client)

            # when
            response = await auth_client.profile(token)

            # then
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.it(
        f"Should return {status.HTTP_401_UNAUTHORIZED} "
        "UNAUTHORIZED when user not found"
    )
    async def test_profile_unauthorized_user_not_found(self) -> None:
        secret_key = secrets.token_hex(64)
        env = {"SECRET_KEY": secret_key}
        async with ServerTest(env) as (http_client, _):
            # given
            user_id = uuid4()
            token = generate_token(user_id, secret_key=secret_key)

            # and
            auth_client = AuthHttpClient(http_client)

            # when
            response = await auth_client.profile(token)

            # then
            assert response.status_code == status.HTTP_401_UNAUTHORIZED
