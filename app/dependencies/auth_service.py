from typing import Annotated

from fastapi import Depends

from app.database.db_session import DatabaseSessionDep
from app.services.auth_service import AuthService


def get_auth_service(session: DatabaseSessionDep):
    return AuthService(session=session)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]