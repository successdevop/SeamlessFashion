from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User
from app.repositories.base import BaseCrud


class UserCrud(BaseCrud[User]):
    def __init__(self, session: AsyncSession ):
        super().__init__(User, session=session)

    async def get_by_email(self, email: str) -> User | None:
        return (
            await self.session.exec(
                select(User).where(User.email == email)
            )
        ).first()

    async def get_by_username(self, username: str) -> User | None:
        return (
            await self.session.exec(
                select(User).where(User.username == username)
            )
        ).one()

    async def get_by_phone_number(self, phone_number: str) -> User | None:
        return (
            await self.session.exec(
                select(User).where(User.phone_number == phone_number)
            )
        ).one()

    async def get_all_active_users(self, is_active: bool = True):
        smt = select(User).where(User.is_active == is_active)
        return (await self.session.exec(smt)).all()