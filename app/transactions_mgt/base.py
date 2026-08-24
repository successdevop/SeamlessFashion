from sqlmodel.ext.asyncio.session import AsyncSession


class UnitOfWork:
    def __init__(self, session: AsyncSession):
        self._session = session

    async def __aenter__(self):
        await self._session.begin()
        return self

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self._session.rollback()
                