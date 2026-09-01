from typing import Annotated

from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.dependencies.auth_service import AuthServiceDep
from app.schemas.identity.user import UserCreate, UserRead, TokenResponse

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@auth_router.post("/sign_up", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def sign_up_user(auth_service: AuthServiceDep, user_data: UserCreate):
    return await auth_service.register_user(user_data=user_data)


@auth_router.post("/sign_in", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def sign_in_user(auth_service: AuthServiceDep, login_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await auth_service.login_user(email=login_data.username, password=login_data.password)


@auth_router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(auth_service: AuthServiceDep, token: str):
    return await auth_service.refresh_token_generation(refresh_token=token)