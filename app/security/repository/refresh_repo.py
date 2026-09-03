from datetime import datetime, timezone
from uuid import UUID

from sqlmodel import select, update
from sqlmodel.ext.asyncio.session import AsyncSession

from app.security.model.refresh_token import RefreshToken


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

    async def get_for_update(self, token_id: UUID) -> RefreshToken | None:
        token = await self._session.exec(
            select(RefreshToken).where(
                RefreshToken.id == token_id
            )
            .with_for_update()
        )
        result = token.one_or_none()
        return result

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

    async def revoke_tokens_by_session(self, session_id: UUID, revoked_at: datetime) -> None:
        stmt = (
            update(RefreshToken).where(
                RefreshToken.session_id == session_id,      #type: ignore
                RefreshToken.revoked_at.is_(None)                       #type: ignore
        ).values(
                revoked_at=revoked_at
            )
        )

        await self._session.exec(stmt)

    async def revoke_token_family(self, family_id: UUID, revoked_at: datetime) -> None:
        stmt = select(RefreshToken).where(RefreshToken.family_token_id == family_id)
        tokens = (await self._session.exec(stmt)).all()

        for token in tokens:
            if token.revoked_at is None:
                token.revoked_at = revoked_at

            if token.used_at is None:
                token.used_at = revoked_at

        await self._session.flush()

    async def delete_token_family(self, family_id: UUID) -> None:
        stmt = select(RefreshToken).where(RefreshToken.family_token_id == family_id)
        tokens = (await self._session.exec(stmt)).all()

        for token in tokens:
            await self._session.delete(instance=token)

        await self._session.flush()

    async def revoke_all_session_tokens_for_user(self, user_id: UUID, revoked_at: datetime):
        stmt = (update(RefreshToken).where(
            RefreshToken.user_id == user_id,    #type: ignore
            RefreshToken.revoked_at.is_(None)               #type: ignore
        )
        .values(
            revoked_at=revoked_at
        ))

        await self._session.exec(stmt)
