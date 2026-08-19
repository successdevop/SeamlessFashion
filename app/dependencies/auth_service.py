from typing import Annotated

from fastapi import Depends

from app.database.db_session import DatabaseSessionDep
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService


def get_user_crud(session: DatabaseSessionDep) -> UserRepository:
    return UserRepository(session=session)


def get_auth_service(crud: Annotated[UserRepository, Depends(get_user_crud)], session: DatabaseSessionDep):
    return AuthService(user_crud=crud, session=session)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]