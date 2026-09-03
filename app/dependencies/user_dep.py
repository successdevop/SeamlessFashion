from typing import Annotated

from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.database.db_session import DatabaseSessionDep
from app.dependencies.auth_service import TokenServiceDep
from app.exceptions.exceptions import InvalidAccessTokenError
from app.models import User
from app.security.schema.auth import CurrentAuth

bearer_scheme = HTTPBearer(auto_error=False)


async def _get_current_auth(
        credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
        token_service: TokenServiceDep
) -> CurrentAuth:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not Authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    try:

        return token_service.parse_access_token(token=str(credentials.credentials))

    except InvalidAccessTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

CurrentAuthDep = Annotated[CurrentAuth, Depends(_get_current_auth)]


async def _get_current_active_user(current_auth: CurrentAuthDep, session: DatabaseSessionDep) -> User:
    user = await session.get(User, current_auth.user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if user.is_deleted:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Inactive User",
            headers={"WWW-Authenticate": "Bearer"}
        )

    return user

CurrentUserDep = Annotated[User, Depends(_get_current_active_user)]
