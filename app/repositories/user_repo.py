from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository[User]):
    def __init__(self, session: AsyncSession ):
        super().__init__(model=User, session=session)

    async def get_by_email_including_deleted(self, email: str) -> User | None:
        return (
            await self._session.exec(
                select(self._model).where(self._model.email == email)
            )
        ).first()

    async def get_by_email(self, email: str) -> User | None:
        return (
            await self._session.exec(
                select(self._model).where(
                    self._model.email == email,
                    self._model.is_deleted.is_(False)
                )
            )
        ).first()

    async def get_by_username(self, username: str) -> User | None:
        return (
            await self._session.exec(
                select(self._model).where(
                    self._model.username == username,
                    self._model.is_deleted.is_(False)
                )
            )
        ).first()

    async def get_by_phone_number(self, phone_number: str) -> User | None:
        return (
            await self._session.exec(
                select(self._model).where(
                    self._model.phone_number == phone_number,
                    self._model.is_deleted.is_(False)
                )
            )
        ).first()

    async def get_users_by_active_status(self, is_active: bool) -> list[User]:
        users = await self._session.exec(
            select(self._model).where(
                self._model.is_active == is_active,
                self._model.is_deleted.is_(False)
            )
        )

        return list(users.all())
