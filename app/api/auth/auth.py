from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth_service import AuthServiceDep
from app.schemas.identity.user import UserCreate, UserRead

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/sign_up", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def sign_up_user(auth_service: AuthServiceDep, user_data: UserCreate):
    return await auth_service.register_user(user_data=user_data)

@auth_router.post("/sign_in")
async def sign_in_user(auth_service: AuthServiceDep, login_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await auth_service.login_user(email=login_data.username, password=login_data.password)
