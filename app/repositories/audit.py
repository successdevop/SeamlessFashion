from sqlmodel.ext.asyncio.session import AsyncSession

from app.schemas.base_or_shared.audit import AuditLogCreate
from base_models.audit import AuditLog


class AuditLogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def save(self, audit_schema: AuditLogCreate) -> AuditLog:
        audit_dict = audit_schema.model_dump(exclude_unset=True)
        new_log = AuditLog(
            **audit_dict
        )
        self.session.add(new_log)
        await self.session.flush()
        return new_log