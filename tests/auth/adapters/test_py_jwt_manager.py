import secrets

import jwt
import pytest
from faker import Faker

from tests.auth.builders.ports.token_payload_builder import TokenPayloadBuilder

from src.auth.adapters.py_jwt_manager import PyJwtManager


@pytest.mark.describe(PyJwtManager.__name__)
class TestPyJwtManager:
    _algorithm = "HS512"
    _secret_key = secrets.token_hex(64)

    @pytest.mark.it("Should encode JWT successfully")
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

    @pytest.mark.it("Should fail when decoding JWT (InvalidSignatureError)")
    def test_decode_jwt_error(self) -> None:
        # given
        encoded_payload = (
            TokenPayloadBuilder().build().model_dump(exclude_none=True)
        )
        token = jwt.encode(
            encoded_payload,
            key=secrets.token_hex(64),
            algorithm=self._algorithm,
        )
        sut = PyJwtManager(self._secret_key, self._algorithm)

        # when
        payload = sut.decode(token)

        # then
        assert payload is None

    @pytest.mark.it("Should fail when decoding JWT (ExpiredSignatureError)")
    def test_decode_expired_signature(self, faker: Faker) -> None:
        # given
        encoded_payload = (
            TokenPayloadBuilder()
            .with_exp(faker.past_datetime())
            .build()
            .model_dump(exclude_none=True)
        )
        token = jwt.encode(
            encoded_payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )
        sut = PyJwtManager(self._secret_key, self._algorithm)

        # when
        payload = sut.decode(token)

        # then
        assert payload is None

    @pytest.mark.it("Should fail when decoding JWT (ImmatureSignatureError)")
    def test_decode_claims_error(self, faker: Faker) -> None:
        # given
        encoded_payload = (
            TokenPayloadBuilder()
            .with_nbf(faker.future_datetime())
            .build()
            .model_dump(exclude_none=True)
        )
        token = jwt.encode(
            encoded_payload,
            key=self._secret_key,
            algorithm=self._algorithm,
        )
        sut = PyJwtManager(self._secret_key, self._algorithm)

        # when
        payload = sut.decode(token)

        # then
        assert payload is None
