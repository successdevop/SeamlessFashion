from datetime import datetime, timezone
from typing import TypeVar, Generic
from uuid import UUID

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, uid: UUID) -> ModelT | None:
        entity = await self.session.get(self.model, uid)
        if entity is None:
            return None

        if getattr(entity, "is_deleted", False):
            return None

        return entity

    async def get_by_id_including_deleted(self, uid: UUID) -> ModelT | None:
        return await self.session.get(self.model, uid)

    async def save(self, entity: ModelT) -> ModelT:
        self.session.add(entity)
        await self.session.flush()
        return entity

    async def refresh(self, entity: ModelT) -> ModelT:
        await self.session.refresh(entity)
        return entity

    async def delete(self, entity: ModelT) -> None:
        if hasattr(entity, "is_deleted"):
            entity.is_deleted = True

            if hasattr(entity, "deleted_at"):
                entity.deleted_at = datetime.now(tz=timezone.utc)

            if hasattr(entity, "is_active"):
                entity.is_active = False

        else:
            await self.session.delete(entity)

        await self.session.flush()

