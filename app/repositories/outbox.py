from sqlmodel.ext.asyncio.session import AsyncSession

from base_models.out_box import OutBoxMessage


class OutBoxRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def add_and_save(self, event_type: str, payload: dict[str, Any]) -> OutBoxMessage:
        message = OutBoxMessage(
            event_type=event_type,
            payload=payload
        )

        self.session.add(message)
        await self.session.flush()
        return message
