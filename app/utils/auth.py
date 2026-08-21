from datetime import datetime, timezone, timedelta
from typing import Optional, Any
from uuid import UUID, uuid4

import jwt
from pwdlib import PasswordHash

from app.database.db_engine import security, PRIVATE_KEY, PUBLIC_KEY

password_hash = PasswordHash.recommended()
DUMMY_HASH = password_hash.hash("dummy_password")


def generate_hash_password(password: str) -> str:
    return password_hash.hash(password=password)


def verify_hash_password(login_password: str, stored_hash_password: str) -> bool:
    return password_hash.verify(password=login_password, hash=stored_hash_password)


def validate_password(password: str) -> tuple[bool, str]:
    special_characters = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    if not any(c.isupper() for c in password) or not any(c.islower() for c in password):
        return False, "Password must contain at least one capital letter and one small letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"

    if not any(c in special_characters for c in password):
        return False, "Password must contain at least one special character"

    return True, "OK"


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
