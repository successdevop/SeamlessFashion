from typing import Annotated

from fastapi import Depends

from app.database.db_session import databaseSessionDep
from app.models import User
from app.services.user_service import UserService


def get_auth_service():
    UserService(User, databaseSessionDep)

authServiceDep = Annotated[UserService, Depends(get_auth_service)]