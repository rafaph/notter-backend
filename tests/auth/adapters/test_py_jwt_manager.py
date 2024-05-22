import secrets

import jwt
import pytest
from faker import Faker

from tests.auth.builders.ports.token_payload_builder import TokenPayloadBuilder

from src.auth.adapters.errors import JwtError
from src.auth.adapters.py_jwt_manager import PyJwtManager


@pytest.mark.describe(PyJwtManager.__name__)
class TestPyJwtManager:
    _algorithm = "HS512"
    _secret_key = secrets.token_hex(64)

    @pytest.mark.it("Should generate JWT successfully")
    def test_generate_jwt(self) -> None:
        # given
        payload = TokenPayloadBuilder().build()
        sut = PyJwtManager(self._secret_key, self._algorithm)
        expected_token = jwt.encode(
            payload.model_dump(exclude_none=True),
            key=self._secret_key,
            algorithm=self._algorithm,
        )

        # when
        token = sut.encode(payload)

        # then
        assert token == expected_token

    @pytest.mark.it("Should decode JWT successfully")
    def test_decode_jwt(self) -> None:
        # given
        payload = TokenPayloadBuilder().build()
        token = jwt.encode(
            payload.model_dump(exclude_none=True),
            key=self._secret_key,
            algorithm=self._algorithm,
        )
        sut = PyJwtManager(self._secret_key, self._algorithm)

        # when
        decoded_payload = sut.decode(token)

        # then
        assert decoded_payload == payload

    @pytest.mark.it("Should decode JWT failure (InvalidSignatureError)")
    def test_decode_jwt_error(self) -> None:
        # given
        payload = TokenPayloadBuilder().build()
        token = jwt.encode(
            payload.model_dump(exclude_none=True),
            key=secrets.token_hex(64),
            algorithm=self._algorithm,
        )
        sut = PyJwtManager(self._secret_key, self._algorithm)

        # when/then
        with pytest.raises(JwtError) as exc_info:
            sut.decode(token)

        # and
        assert isinstance(
            exc_info.value.error,
            jwt.exceptions.InvalidSignatureError,
        )
        assert str(exc_info.value) == "Signature verification failed"

    @pytest.mark.it("Should decode JWT failure (ExpiredSignatureError)")
    def test_decode_expired_signature(self, faker: Faker) -> None:
        # given
        payload = TokenPayloadBuilder().with_exp(faker.past_datetime()).build()
        token = jwt.encode(
            payload.model_dump(exclude_none=True),
            key=self._secret_key,
            algorithm=self._algorithm,
        )
        sut = PyJwtManager(self._secret_key, self._algorithm)

        # when/then
        with pytest.raises(JwtError) as exc_info:
            sut.decode(token)

        # and
        assert isinstance(
            exc_info.value.error,
            jwt.exceptions.ExpiredSignatureError,
        )
        assert str(exc_info.value) == "Signature has expired"

    @pytest.mark.it("Should decode JWT failure (ImmatureSignatureError)")
    def test_decode_claims_error(self, faker: Faker) -> None:
        # given
        payload = (
            TokenPayloadBuilder().with_nbf(faker.future_datetime()).build()
        )
        token = jwt.encode(
            payload.model_dump(exclude_none=True),
            key=self._secret_key,
            algorithm=self._algorithm,
        )
        sut = PyJwtManager(self._secret_key, self._algorithm)

        # when/then
        with pytest.raises(JwtError) as exc_info:
            sut.decode(token)

        # and
        assert isinstance(
            exc_info.value.error,
            jwt.exceptions.ImmatureSignatureError,
        )
        assert str(exc_info.value) == "The token is not yet valid (nbf)"
