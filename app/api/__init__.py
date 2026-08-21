from fastapi import APIRouter

from app.api.auth.auth import auth_router

api_routes = APIRouter()
api_routes.include_router(auth_router)
