from collections.abc import AsyncGenerator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncEngine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.database.db_engine import db_settings


engine: AsyncEngine = create_async_engine(
    url=db_settings.postgres_url,
    echo=db_settings.DB_ECHO,
    pool_pre_ping=True
)


AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


DatabaseSessionDep = Annotated[AsyncSession, Depends(get_db_session)]