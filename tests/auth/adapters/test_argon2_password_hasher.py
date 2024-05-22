from unittest.mock import MagicMock

import argon2
import pytest
from faker import Faker

from src.auth.adapters.argon2_password_hasher import Argon2PasswordHasher
from src.auth.adapters.errors import HashingError


@pytest.fixture(name="password_hasher")
def fixture_password_hasher(faker: Faker) -> MagicMock:
    password_hasher = MagicMock(spec=argon2.PasswordHasher)
    password_hasher.verify.return_value = True
    password_hasher.hash.return_value = str(faker.sha256())
    password_hasher.check_needs_rehash.return_value = True
    return password_hasher


@pytest.mark.describe(Argon2PasswordHasher.__name__)
class TestArgon2PasswordHasher:
    @pytest.mark.it("Should verify password successfully")
    def test_verify_success(
        self,
        faker: Faker,
        password_hasher: MagicMock,
    ) -> None:
        # given
        password = faker.password()
        hash_ = str(faker.sha256())
        sut = Argon2PasswordHasher(password_hasher)

        # when
        result = sut.verify(hash_, password)

        # then
        assert result
        password_hasher.verify.assert_called_once_with(hash_, password)

    @pytest.mark.parametrize(
        "side_effect",
        [
            [argon2.exceptions.InvalidHashError()],
            [argon2.exceptions.VerificationError()],
            [argon2.exceptions.VerifyMismatchError()],
        ],
        ids=["InvalidHashError", "VerificationError", "VerifyMismatchError"],
    )
    @pytest.mark.it("Should NOT verify successfully with exception")
    def test_verify_fail(
        self,
        faker: Faker,
        password_hasher: MagicMock,
        side_effect: Exception,
    ) -> None:
        # given
        password = faker.password()
        hash_ = str(faker.sha256())
        password_hasher.verify.side_effect = side_effect
        sut = Argon2PasswordHasher(password_hasher)

        # when
        result = sut.verify(hash_, password)

        # then
        assert not result
        password_hasher.verify.assert_called_once_with(hash_, password)

    @pytest.mark.it("Should hash password successfully")
    def test_hash_success(
        self,
        faker: Faker,
        password_hasher: MagicMock,
    ) -> None:
        # given
        password = faker.password()
        hash_ = password_hasher.hash.return_value
        sut = Argon2PasswordHasher(password_hasher)

        # when
        result = sut.hash(password)

        # then
        assert result == hash_
        password_hasher.hash.assert_called_once_with(password)

    @pytest.mark.it("Should NOT hash password successfully")
    def test_hash_fail(
        self,
        faker: Faker,
        password_hasher: MagicMock,
    ) -> None:
        # given
        password = faker.password()
        password_hasher.hash.side_effect = argon2.exceptions.HashingError()
        sut = Argon2PasswordHasher(password_hasher)

        # when/then
        with pytest.raises(HashingError) as exc_info:
            sut.hash(password)

        # and
        assert str(exc_info.value) == ""

        # and
        exc = exc_info.value.error
        assert isinstance(exc, argon2.exceptions.HashingError)
        password_hasher.hash.assert_called_once_with(password)

    @pytest.mark.it("Should check if needs rehash successfully")
    def test_needs_rehash_success(
        self,
        faker: Faker,
        password_hasher: MagicMock,
    ) -> None:
        # given
        hash_ = str(faker.sha256())
        sut = Argon2PasswordHasher(password_hasher)

        # when
        result = sut.needs_rehash(hash_)

        # then
        assert result
        password_hasher.check_needs_rehash.assert_called_once_with(hash_)
