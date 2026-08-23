from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.transactions_mgt.base import UnitOfWork
from app.repositories.user_repo import UserRepository


class AuthUnitOfWork(UnitOfWork):
    def __init__(self, session: AsyncSession):
        super().__init__(session=session)

        self.users = UserRepository(session=session)