from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession ):
        super().__init__(User, session=session)

    async def get_by_email(self, email: str) -> User | None:
        user = (
            await self.session.exec(
                select(User).where(User.email == email)
            )
        ).first()

        if user is None:
            return None

        if user.__getattribute__("is_deleted", True):
            return None

        return user

    async def get_by_username(self, username: str) -> User | None:
        user = (
            await self.session.exec(
                select(User).where(User.username == username)
            )
        ).first()

        if user is None:
            return None

        if user.__getattribute__("is_deleted", True):
            return None

        return user

    async def get_by_phone_number(self, phone_number: str) -> User | None:
        user = (
            await self.session.exec(
                select(User).where(User.phone_number == phone_number)
            )
        ).first()

        if user is None:
            return None

        if user.__getattribute__("is_deleted", True):
            return None

        return user

    async def get_users_by_active_status(self, is_active: bool) -> list[User]:
        users = await self.session.exec(
            select(User).where(User.is_active == is_active)
        )

        return list(users.all())
