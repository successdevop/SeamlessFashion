from typing import Any

from sqlmodel.ext.asyncio.session import AsyncSession

from base_models.out_box import OutboxMessage


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
