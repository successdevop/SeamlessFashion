from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.user_repo import UserCrud
from app.schemas.identity.user import UserCreate


class UserService(UserCrud):
    def __init__(self, model: SQLModel, session: AsyncSession):
        super().__init__(model=model, session=session)

    def register_user(self, user: UserCreate):
        pass