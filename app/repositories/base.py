from typing import TypeVar, Generic, Optional
from uuid import UUID

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseCrud(Generic[ModelT]):
    def __init__(self, model: type[ModelT], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def _get_by_id(self, uid: UUID) -> Optional[ModelT]:
        return await self.session.get(self.model, uid)

    async def _save(self, entity: SQLModel):
        self.session.add(entity)
        await self.session.commit()
        await self.session.refresh(entity)
        return entity

    async def _update(self, entity: SQLModel):
        self.session.add(entity)
        await self.session.commit()
        return entity

    async def _delete(self, entity: SQLModel):
        await self.session.delete(entity)
        await self.session.commit()


