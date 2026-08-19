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
        return await self.session.get(self.model, uid)

    async def save(self, entity: ModelT) -> None:
        self.session.add(entity)
        await self.session.flush()

    async def delete(self, entity: ModelT) -> None:
        await self.session.delete(entity)
        await self.session.flush()

    async def soft_delete(self, entity: ModelT) -> None:
        if all(hasattr(entity, field) for field in ("is_deleted", "deleted_at", "is_active")):
            entity.is_deleted = True
            entity.deleted_at = datetime.now(tz=timezone.utc)
            entity.is_active = False
        elif all(hasattr(entity, field) for field in ("is_deleted", "deleted_at")):
            entity.is_deleted = True
            entity.deleted_at = datetime.now(tz=timezone.utc)
        else:
            raise ValueError(f"{self.model.__name__} does not support soft deletion")
        await self.session.flush()
