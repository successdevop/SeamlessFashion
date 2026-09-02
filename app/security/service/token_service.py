from dataclasses import dataclass
from datetime import timedelta, datetime, timezone
from enum import StrEnum
from typing import Any
from uuid import UUID, uuid4

import jwt
from jwt import InvalidTokenError


@dataclass(frozen=True)
class SigningKey:
    kid: str
    private_key: str
    public_key: str
    algorithm: str


class KeyManager:
    def __init__(self, current_kid: str, private_key: str, public_key: str, algorithm: str) -> None:
        self._current_kid = current_kid
        self._keys = {
            current_kid: SigningKey(
                kid=current_kid, private_key=private_key, public_key=public_key, algorithm=algorithm
            )
        }

    @property
    def current_kid(self):
        return self._current_kid

    def get_current_signing_key(self):
        return self._keys[self._current_kid]

    def get_public_key(self, kid: str):
        key = self._keys.get(kid)

        if key is None:
            return None

        return key.public_key


class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"


class TokenService:
    def __init__(
            self,
            key_manager: KeyManager,
            issuer: str,
            audience: str,
            access_token_lifetime: int,
            refresh_token_lifetime: int
    ) -> None:
        self.key_manager = key_manager
        self.issuer = issuer
        self.audience = audience
        self.access_token_lifetime = access_token_lifetime
        self.refresh_token_lifetime = refresh_token_lifetime

    def create_access_token(self, user_id: UUID, session_id: UUID) -> str:
        now = datetime.now(tz=timezone.utc)

        expires_at = now + timedelta(minutes=self.access_token_lifetime)
        jti = str(uuid4())
        key = self.key_manager.get_current_signing_key()

        payload = {
            "sub": str(user_id),
            "sid": str(session_id),
            "iss": self.issuer,
            "aud": self.audience,
            "iat": now,
            "nbf": now,
            "exp": expires_at,
            "jti": jti,
            "type": TokenType.ACCESS
        }

        token = jwt.encode(
            payload=payload,
            key=key.private_key,
            algorithm=key.algorithm,
            headers={
                "kid": key.kid,
                "type": "JWT"
            }
        )

        return token

    def create_refresh_token(self, user_id: UUID, session_id: UUID, family_token_id: UUID, token_id: UUID) -> str:
        now = datetime.now(tz=timezone.utc)

        expires_at = now + timedelta(days=self.refresh_token_lifetime)
        jti = str(token_id)
        key = self.key_manager.get_current_signing_key()

        payload = {
            "sub": str(user_id),
            "iss": self.issuer,
            "aud": self.audience,
            "iat": now,
            "nbf": now,
            "exp": expires_at,
            "jti": jti,
            "type": TokenType.REFRESH,
            "sid": str(session_id),
            "fid": str(family_token_id)
        }

        return jwt.encode(
            payload=payload,
            key=key.private_key,
            algorithm=key.algorithm,
            headers={
                "kid": key.kid,
                "type": "JWT"
            }
        )

    def decode_access_token(self, token: str) -> dict[str, Any]:
        payload = self._decode(token=token)
        if payload.get("type") != TokenType.ACCESS:
            raise InvalidTokenError("Invalid token type")
        return payload

    def decode_refresh_token(self, token: str) -> dict[str, Any]:
        payload = self._decode(token=token)
        if payload.get("type") != TokenType.REFRESH:
            raise InvalidTokenError("Invalid token type")

        return payload

    def _decode(self, token: str) -> dict[str, Any]:
        kid = self._get_kid(token=token)

        public_key = self.key_manager.get_public_key(kid=kid)

        if public_key is None:
            raise InvalidTokenError("Unknown signing key")

        algorithm = self.key_manager.get_current_signing_key().algorithm

        try:
            return jwt.decode(
                jwt=token,
                key=public_key,
                algorithms=[algorithm],
                issuer=self.issuer,
                audience=self.audience,
                options={
                    "require": ["sub",
                                "iss",
                                "aud",
                                "iat",
                                "nbf",
                                "exp",
                                "jti",
                                "type"]
                }
            )
        except InvalidTokenError:
            raise

    def _get_kid(self, token: str) -> str:
        header = jwt.get_unverified_header(token)

        kid = header.get("kid")
        if not kid:
            raise InvalidTokenError("Missing key identifier")

        return kid
