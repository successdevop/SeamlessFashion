from datetime import datetime, timezone
from typing import TypeVar, Generic, Optional
from uuid import UUID

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession


ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseCrud(Generic[ModelT]):
    def __init__(self, model: type[ModelT], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, uid: UUID) -> Optional[ModelT]:
        return await self.session.get(self.model, uid)

    async def save(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        await self.session.flush()
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity: ModelT, soft_delete: bool = True) -> None:
        if soft_delete and hasattr(entity, "is_deleted"):
            entity.is_deleted = True
            entity.deleted_at = datetime.now(tz=timezone.utc)
            entity.is_active = False
        else:
            await self.session.delete(entity)

        await self.session.flush()
