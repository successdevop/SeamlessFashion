from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession ):
        super().__init__(model=User, session=session)

    async def get_by_email_including_deleted(self, email: str) -> User | None:
        return (
            await self.session.exec(
                select(self.model).where(self.model.email == email)
            )
        ).first()

    async def get_by_email(self, email: str) -> User | None:
        return (
            await self.session.exec(
                select(self.model).where(
                    self.model.email == email,
                    self.model.is_deleted.is_(False)
                )
            )
        ).first()

    async def get_by_username(self, username: str) -> User | None:
        return (
            await self.session.exec(
                select(self.model).where(
                    self.model.username == username,
                    self.model.is_deleted.is_(False)
                )
            )
        ).first()

    async def get_by_phone_number(self, phone_number: str) -> User | None:
        return (
            await self.session.exec(
                select(self.model).where(
                    self.model.phone_number == phone_number,
                    self.model.is_deleted.is_(False)
                )
            )
        ).first()

    async def get_users_by_active_status(self, is_active: bool) -> list[User]:
        users = await self.session.exec(
            select(self.model).where(self.model.is_active == is_active)
        )

        return list(users.all())
