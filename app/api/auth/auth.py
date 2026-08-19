from fastapi import APIRouter

from app.dependencies.auth_service import authServiceDep
from app.schemas.identity.user import UserCreate

auth = APIRouter()

@auth.post("/register")
async def register_user(auth_service: authServiceDep, req_body: UserCreate):
    return await auth_service.register_user(user_data=req_body)