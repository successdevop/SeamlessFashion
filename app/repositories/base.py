from datetime import datetime, timezone
from typing import TypeVar, Generic
from uuid import UUID

from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models import User

ModelT = TypeVar("ModelT", bound=SQLModel)


class BaseRepository(Generic[ModelT]):
    def __init__(self, model: type[ModelT], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get_by_id(self, uid: UUID) -> ModelT | None:
        entity = await self.session.get(self.model, uid)
        if entity is None:
            return None

        if getattr(entity, "is_deleted", True):
            return None

        return entity

    async def get_by_id_including_deleted(self, uid: UUID) -> ModelT | None:
        return await self.session.get(self.model, uid)

    async def save(self, entity: ModelT) -> None:
        self.session.add(entity)
        await self.session.flush()

    async def delete(self, entity: ModelT) -> None:
        if isinstance(entity, User):
            entity.is_deleted = True
            entity.deleted_at = datetime.now(tz=timezone.utc)
            entity.is_active = False
        elif hasattr(entity, "is_deleted"):
            entity.is_deleted = True
            entity.deleted_at = datetime.now(tz=timezone.utc)
        else:
            await self.session.delete(entity)

        await self.session.flush()

