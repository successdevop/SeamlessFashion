from sqlmodel.ext.asyncio.session import AsyncSession

from app.repositories.audit import AuditLogRepository
from app.transactions_mgt.base import UnitOfWork
from app.repositories.outbox import OutboxRepository
from app.repositories.user_repo import UserRepository


class AuthUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

        self.users = UserRepository(session=session)
        self.outbox_message = OutboxRepository(session=session)
        self.audit_log = AuditLogRepository(session=session)