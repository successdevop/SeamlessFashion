from datetime import datetime, timezone, timedelta
from typing import Optional, Any
from uuid import UUID, uuid4

import jwt
from pwdlib import PasswordHash

from app.config.config import security, PRIVATE_KEY, PUBLIC_KEY

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy_password")


def generate_hash_password(password: str) -> str:
    return password_hash.hash(password=password)


def verify_hash_password(login_password: str, stored_hash_password: str) -> bool:
    return password_hash.verify(password=login_password, hash=stored_hash_password)


def generate_access_token(user_id: UUID) -> str:
    now = datetime.now(tz=timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES),
        "type": "access",
        "jti": str(uuid4())
    }

    return jwt.encode(
        payload=payload, key=PRIVATE_KEY, algorithm=security.JWT_ALGORITHM
    )


def generate_refresh_token(user_id: UUID) -> str:
    now = datetime.now(tz=timezone.utc)

    payload = {
        "sub": str(user_id),
        "iat": now,
        "exp": now + timedelta(days=security.REFRESH_TOKEN_EXPIRE_DAYS),
        "type": "refresh",
        "jti": str(uuid4())
    }

    return jwt.encode(
        payload=payload, key=PRIVATE_KEY, algorithm=security.JWT_ALGORITHM
    )


def decode_token(token: str) -> Optional[dict[str, Any]]:
    try:
        return jwt.decode(
            jwt=token,
            key=PUBLIC_KEY,
            algorithms=[security.JWT_ALGORITHM]
        )
    except jwt.PyJWTError:
        return None
