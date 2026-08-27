from datetime import datetime, timezone
from typing import Any

from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.enums.user_enums import OutboxStatus
from app.models.base_models.out_box import OutboxMessage


class OutboxRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_and_flush(self, event_type: str, payload: dict[str, Any]) -> OutboxMessage:
        message = OutboxMessage(
            event_type=event_type,
            payload=payload
        )

        self._session.add(message)
        await self._session.flush()
        return message

    async def claim_messages(self, limit: int = 100) -> list[OutboxMessage]:
        stmt = (
            select(OutboxMessage).where(
                OutboxMessage.status == OutboxStatus.PENDING,
                OutboxMessage.available_at <= datetime.now(tz=timezone.utc),
            )
            .order_by(OutboxMessage.created_at)
            .limit(limit)
            .with_for_update(skip_locked=True)
        )

        result = await self._session.exec(stmt)

        messages = list(result.all())

        for message in messages:
            message.status = OutboxStatus.PROCESSING
            message.attempts += 1

        await self._session.commit()
        return messages
