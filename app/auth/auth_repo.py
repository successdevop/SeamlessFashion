from datetime import datetime, timezone
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.auth_session import AuthSession, AuthSessionStatus


class AuthSessionRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_and_flush(self, auth_session: AuthSession) -> AuthSession:
        session_dict = auth_session.model_dump()

        new_session = AuthSession(
            **session_dict
        )

        self._session.add(new_session)
        await self._session.flush()
        return new_session

    async def get_session_by_id(self, session_id: UUID) -> AuthSession | None:
        return await self._session.get(AuthSession, session_id) #type:ignore

    async def get_session_for_update(self, session_id: UUID) -> AuthSession | None:
        return (
            await self._session.exec(
                select(AuthSession).where(AuthSession.id == session_id)
                .with_for_update(skip_locked=True)
            )
        ).first()

    async def get_by_id_for_user(self, user_id: UUID, session_id: UUID) -> AuthSession | None:
        session = await self._session.exec(
            select(AuthSession).where(
                AuthSession.id == session_id,
                AuthSession.user_id == user_id
            )
            .with_for_update(skip_locked=True)
        )

        return session.one_or_none()

