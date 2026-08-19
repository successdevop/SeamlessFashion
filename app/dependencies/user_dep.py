from typing import Annotated, Any
from uuid import UUID

from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.database.db_session import databaseSessionDep
from app.models import User
from app.utils.auth import decode_token


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def _get_access_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, Any]:
    token_data = decode_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=403,
            detail="Invalid or expired token"
        )

    return token_data


def _get_user_id_from_access_token(token_data: Annotated[dict, Depends(_get_access_token)]) -> UUID:
    user_id = UUID(token_data.get("sub"))
    return user_id


async def _get_active_user(
        user_id: Annotated[UUID, Depends(_get_user_id_from_access_token)],
        session: databaseSessionDep
):
    user = await session.get(User, user_id)
    if user is None:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="could not validate credentials")

    if not user.is_active:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")
    return user