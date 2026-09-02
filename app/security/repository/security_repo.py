from sqlmodel.ext.asyncio.session import AsyncSession

from app.auth.model.security_event import SecurityEvent


class SecurityRepository:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def add_and_flush(self, security_data: SecurityEvent) -> SecurityEvent:
        security_dict = security_data.model_dump()

        new_security_event = SecurityEvent(
            **security_dict
        )

        self._session.add(new_security_event)
        await self._session.flush()
        return new_security_event