from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import update
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.base import BaseRepository
from app.security.model.auth_session import AuthSession
from app.security.schema.auth import AuthSessionStatus


class AuthSessionRepository(BaseRepository[AuthSession]):
    def __init__(self, session: AsyncSession):
        super().__init__(model=AuthSession, session=session)
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

    async def revoke_a_session(self, auth_session: AuthSession, reason: str) -> None:
        auth_session.status = AuthSessionStatus.REVOKED
        auth_session.revoked_at = datetime.now(tz=timezone.utc)
        auth_session.revoked_reason = reason

        await self._session.flush()

    async def revoke_all_session_for_user(self, user_id: UUID, revoked_at: datetime, revoked_reason: str):
        stmt = (
            update(AuthSession).where(
                AuthSession.user_id == user_id,    #type: ignore
                AuthSession.revoked_at.is_(None)               #type: ignore
            )
            .values(                                           #type: ignore
                revoked_at=revoked_at,
                revoked_reason=revoked_reason
            )
        )

        await self._session.exec(stmt)

    async def get_all_sessions_by_user_id(self, user_id: UUID):
        stmt = (
            select(AuthSession).where(
                AuthSession.user_id == user_id,
                AuthSession.revoked_at.is_(None)
            )
        )

        sessions = (await self._session.exec(stmt)).all()
        return sessions
