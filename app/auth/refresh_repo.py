from datetime import datetime, timezone
from uuid import UUID

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.auth_session import AuthSession, AuthSessionStatus
from app.auth.refresh_token import RefreshToken


class RefreshTokenRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_and_flush(self, token: RefreshToken) -> RefreshToken:
        token_dict = token.model_dump()

        new_token = RefreshToken(
            **token_dict
        )

        self._session.add(new_token)
        await self._session.flush()
        return new_token

    async def get_refresh_token_by_hash_for_updated(self, token_hash: str) -> RefreshToken | None:
        return (
            await self._session.exec(
                select(RefreshToken).where(RefreshToken.token_hash == token_hash)
                .with_for_update(skip_locked=True)
            )
        ).first()

    async def mark_refresh_token_as_used(self, token: RefreshToken) -> None:
        token.used_at = datetime.now(tz=timezone.utc)
        await self._session.flush()

    # not clear about this function yet
    async def replace_refresh_token(self, new_token: RefreshToken) -> None:
        new_token.replaced_by_token_id = new_token.id
        await self._session.flush()

    async def revoke_a_session(self, auth_session: AuthSession, reason: str) -> None:
        auth_session.status = AuthSessionStatus.REVOKED
        auth_session.revoked_at = datetime.now(tz=timezone.utc)
        auth_session.revoked_reason = reason

        await self._session.flush()

    async def revoke_token_family(self, token_family_id: UUID):

