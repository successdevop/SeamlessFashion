from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.base_or_shared.audit import AuditLogCreate
from app.models.base_models.audit import AuditLog


class AuditLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def add_and_flush(self, audit_schema: AuditLogCreate) -> AuditLog:
        audit_dict = audit_schema.model_dump(mode="json", exclude_unset=True)
        new_log = AuditLog(
            **audit_dict
        )
        self._session.add(new_log)
        await self._session.flush()
        return new_log