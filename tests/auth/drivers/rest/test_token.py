import argon2
import pytest
from faker import Faker
from fastapi import status

from tests.auth.builders.domain.entities.user_builder import UserBuilder
from tests.auth.helpers.auth_database_client import AuthDatabaseClient
from tests.auth.helpers.auth_http_client import AuthHttpClient
from tests.helpers.server_test import ServerTest


@pytest.mark.anyio(scope="class")
@pytest.mark.describe("POST /auth/token")
class TestToken:
    @pytest.mark.it(f"Should return {status.HTTP_200_OK} OK")
    async def test_token_ok(self, faker: Faker) -> None:
        async with ServerTest() as (http_client, pool):
            # given
            password_hasher = argon2.PasswordHasher()
            raw_password = faker.password()
            password = password_hasher.hash(raw_password)
            user = UserBuilder().with_password(password).build()

            # and
            auth_database_client = AuthDatabaseClient(pool)
            await auth_database_client.create_user(user)

            # and
            auth_client = AuthHttpClient(http_client)
            body: dict[str, object] = {
                "username": user.email,
                "password": raw_password,
            }

            # when
            response = await auth_client.token(body)

            # then
            assert response.status_code == status.HTTP_200_OK

            # and
            data = response.json()
            assert "access_token" in data
            assert "token_type" in data

    @pytest.mark.it(
        f"Should return {status.HTTP_401_UNAUTHORIZED} "
        "UNAUTHORIZED when user does not exist",
    )
    async def test_token_unauthorized_user_not_found(
        self,
        faker: Faker,
    ) -> None:
        async with ServerTest() as (http_client, _):
            # given
            auth_client = AuthHttpClient(http_client)
            body: dict[str, object] = {
                "username": faker.email(),
                "password": faker.password(),
            }

            # when
            response = await auth_client.token(body)

            # then
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # and
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "Invalid credentials"

    @pytest.mark.it(
        f"Should return {status.HTTP_401_UNAUTHORIZED} "
        "UNAUTHORIZED when user password is wrong",
    )
    async def test_token_unauthorized_password(self, faker: Faker) -> None:
        async with ServerTest() as (http_client, pool):
            # given
            password_hasher = argon2.PasswordHasher()
            raw_password = faker.password()
            password = password_hasher.hash(raw_password)
            user = UserBuilder().with_password(password).build()

            # and
            auth_database_client = AuthDatabaseClient(pool)
            await auth_database_client.create_user(user)

            # and
            auth_client = AuthHttpClient(http_client)
            body: dict[str, object] = {
                "username": user.email,
                "password": faker.password(),
            }

            # when
            response = await auth_client.token(body)

            # then
            assert response.status_code == status.HTTP_401_UNAUTHORIZED

            # and
            data = response.json()
            assert "detail" in data
            assert data["detail"] == "Invalid credentials"
