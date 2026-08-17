from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.base import BaseCrud


class UserCrud(BaseCrud):
    def __init__(self, model: SQLModel, session: AsyncSession ):
        super().__init__(model=type[model], session=session)

    async def get_by_email(self, email: str):
        return (
            await self.session.exec(
                select(self.model).where(self.model.email == email)
            )
        ).one()

    async def get_by_username(self, username: str):
        return (
            await self.session.exec(
                select(self.model).where(self.model.username == username)
            )
        ).one()

    async def get_by_phone_number(self, phone_number: str):
        return (
            await self.session.exec(
                select(self.model).where(self.model.phone_number == phone_number)
            )
        ).one()

    async def get_all_active_users(self, is_active: bool = True):
        return (
            await self.session.exec(
                select(self.model).where(self.model.is_active == is_active)
            )
        ).all()