from datetime import datetime, timezone
from typing import TypeVar, Generic
from uuid import UUID

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT], session: AsyncSession) -> None:
        self._model = model
        self._session = session

    async def get_by_id_including_deleted(self, uid: UUID) -> ModelT | None:
        return await self._session.get(self._model, uid)

    async def get_by_id(self, uid: UUID) -> ModelT | None:
        entity = await self._session.get(self._model, uid)
        if entity is None:
            return None

        if getattr(entity, "is_deleted", False):
            return None

        return entity

    async def add_and_flush(self, entity: ModelT) -> ModelT:
        self._session.add(entity)
        await self._session.flush()
        return entity

    async def delete_and_flush(self, entity: ModelT) -> None:
        if hasattr(entity, "is_deleted"):
            entity.is_deleted = True

            if hasattr(entity, "deleted_at"):
                entity.deleted_at = datetime.now(tz=timezone.utc)

            if hasattr(entity, "is_active"):
                entity.is_active = False

        else:
            await self._session.delete(entity)

        await self._session.flush()

