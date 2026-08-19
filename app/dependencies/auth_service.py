from typing import Annotated

from fastapi import Depends

from app.database.db_session import DatabaseSessionDep
from app.repositories.user_repo import UserCrud
from app.services.auth_service import AuthService


def get_user_crud(session: DatabaseSessionDep) -> UserCrud:
    return UserCrud(session=session)


def get_auth_service(crud: Annotated[UserCrud, Depends(get_user_crud)]):
    return AuthService(user_crud=crud)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]