from typing import Annotated

from fastapi import Depends

from app.database.db_session import DatabaseSessionDep
from app.services.auth_service import AuthService
from app.transactions_mgt.auth import AuthUnitOfWork


def get_auth_service(session: DatabaseSessionDep):
    auth = AuthUnitOfWork(session=session)
    return AuthService(auth=auth)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]