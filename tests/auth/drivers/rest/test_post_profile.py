import secrets

import pytest
from faker import Faker
from fastapi import status

from tests.auth.builders.domain.entities.user_builder import UserBuilder
from tests.auth.helpers.auth_database_client import AuthDatabaseClient
from tests.auth.helpers.auth_http_client import AuthHttpClient
from tests.auth.helpers.generate_token import generate_token
from tests.helpers.server_test import ServerTest


@pytest.mark.anyio(scope="class")
@pytest.mark.describe("POST /auth/profile")
class TestPostProfile:
    @pytest.mark.it(
        f"Should return {status.HTTP_200_OK} OK (all fields updated)"
    )
    async def test_profile_ok_all_fields(self, faker: Faker) -> None:
        secret_key = secrets.token_hex(64)
        env = {"JWT_SECRET_KEY": secret_key}
        async with ServerTest(env) as (http_client, pool):
            # given
            auth_database_client = AuthDatabaseClient(pool)
            auth_client = AuthHttpClient(http_client)

            # and
            raw_password = faker.password()
            current_user = (
                UserBuilder().with_hashed_password(raw_password).build()
            )
            await auth_database_client.create_user(current_user)

            # and
            token = generate_token(current_user.id, secret_key=secret_key)

            # and
            password = faker.password()
            body = {
                **UserBuilder()
                .build()
                .model_dump(
                    mode="json",
                    exclude={
                        "id",
                        "updated_at",
                        "created_at",
                    },
                ),
                "password": password,
                "password_confirmation": password,
            }

            # when
            response = await auth_client.post_profile(token, body)

            # then
            assert response.status_code == status.HTTP_200_OK

            # and
            user_from_db = await auth_database_client.select_user(
                current_user.id
            )
            assert user_from_db is not None
            user_dict = user_from_db.model_dump(mode="json")

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
            for field in fields:
                assert field in output
                assert field in user_dict
                assert output[field] == user_dict[field]

            # and
            assert set(fields) == set(output.keys())

    @pytest.mark.it(f"Should return {status.HTTP_200_OK} OK (without email)")
    async def test_profile_ok_no_email(self, faker: Faker) -> None:
        secret_key = secrets.token_hex(64)
        env = {"JWT_SECRET_KEY": secret_key}
        async with ServerTest(env) as (http_client, pool):
            # given
            auth_database_client = AuthDatabaseClient(pool)
            auth_client = AuthHttpClient(http_client)

            # and
            raw_password = faker.password()
            current_user = (
                UserBuilder().with_hashed_password(raw_password).build()
            )
            await auth_database_client.create_user(current_user)

            # and
            token = generate_token(current_user.id, secret_key=secret_key)

            # and
            password = faker.password()
            body = {
                **UserBuilder()
                .build()
                .model_dump(
                    mode="json",
                    exclude={
                        "id",
                        "email",
                        "updated_at",
                        "created_at",
                    },
                ),
                "password": password,
                "password_confirmation": password,
            }

            # when
            response = await auth_client.post_profile(token, body)

            # then
            assert response.status_code == status.HTTP_200_OK

            # and
            user_from_db = await auth_database_client.select_user(
                current_user.id
            )
            assert user_from_db is not None
            user_dict = user_from_db.model_dump(mode="json")

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
            for field in fields:
                assert field in output
                assert field in user_dict
                assert output[field] == user_dict[field]

            # and
            assert set(fields) == set(output.keys())

    @pytest.mark.it(
        f"Should return {status.HTTP_401_UNAUTHORIZED} UNAUTHORIZED"
    )
    async def test_profile_not_authorized(self) -> None:
        async with ServerTest() as (http_client, _):
            # given
            auth_client = AuthHttpClient(http_client)

            # when
            response = await auth_client.post_profile()

            # then
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.it(f"Should return {status.HTTP_409_CONFLICT} CONFLICT")
    async def test_profile_conflict(self, faker: Faker) -> None:
        secret_key = secrets.token_hex(64)
        env = {"JWT_SECRET_KEY": secret_key}
        async with ServerTest(env) as (http_client, pool):
            # given
            auth_database_client = AuthDatabaseClient(pool)
            auth_client = AuthHttpClient(http_client)

            # and
            raw_password = faker.password()
            current_user = (
                UserBuilder().with_hashed_password(raw_password).build()
            )
            await auth_database_client.create_user(current_user)

            # and
            another_user = UserBuilder().build()
            await auth_database_client.create_user(another_user)

            # and
            token = generate_token(current_user.id, secret_key=secret_key)

            # and
            body: dict[str, object] = {
                "email": another_user.email,
            }

            # when
            response = await auth_client.post_profile(token, body)

            # then
            assert response.status_code == status.HTTP_409_CONFLICT

    @pytest.mark.it(
        f"Should return {status.HTTP_422_UNPROCESSABLE_ENTITY} "
        "UNPROCESSABLE_ENTITY"
    )
    async def test_profile_unprocessable_entity(self, faker: Faker) -> None:
        secret_key = secrets.token_hex(64)
        env = {"JWT_SECRET_KEY": secret_key}
        async with ServerTest(env) as (http_client, pool):
            # given
            auth_database_client = AuthDatabaseClient(pool)
            auth_client = AuthHttpClient(http_client)

            # and
            raw_password = faker.password()
            current_user = (
                UserBuilder().with_hashed_password(raw_password).build()
            )
            await auth_database_client.create_user(current_user)

            # and
            token = generate_token(current_user.id, secret_key=secret_key)

            # and
            body: dict[str, object] = {
                "password": faker.password(),
                "password_confirmation": faker.password(),
            }

            # when
            response = await auth_client.post_profile(token, body)

            # then
            assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
