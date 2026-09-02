from typing import Annotated

from fastapi import Depends

from app.auth.service.passwd_service import PasswordService
from app.auth.service.token_service import TokenService, KeyManager
from app.config.config import security, PRIVATE_KEY, PUBLIC_KEY
from app.database.db_session import DatabaseSessionDep
from app.services.auth_service import AuthService
from app.transactions_mgt.auth import AuthUnitOfWork


key_manager = KeyManager(
    current_kid=security.JWT_CURRENT_KID, private_key=PRIVATE_KEY,
    public_key=PUBLIC_KEY, algorithm=security.JWT_ALGORITHM
)

token_service = TokenService(
    key_manager=key_manager, issuer=security.JWT_ISSUER, audience=security.JWT_AUDIENCE,
    access_token_lifetime=security.ACCESS_TOKEN_EXPIRE_MINUTES,
    refresh_token_lifetime=security.REFRESH_TOKEN_EXPIRE_DAYS
)


def get_auth_service(session: DatabaseSessionDep):
    auth = AuthUnitOfWork(session=session)
    password_service = PasswordService()
    return AuthService(auth=auth, password_service=password_service, token_service=token_service)

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]