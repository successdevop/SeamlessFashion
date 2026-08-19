from fastapi import APIRouter, status

from app.dependencies.auth_service import AuthServiceDep
from app.schemas.identity.user import UserCreate, UserRead

auth = APIRouter()

@auth.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(auth_service: AuthServiceDep, req_body: UserCreate):
    return await auth_service.register_user(user_data=req_body)