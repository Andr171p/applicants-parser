from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from config import settings

from .schemas import ListApplicantsSchema


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    engine = create_async_engine(url=settings.sql_settings.get_db_url, echo=True)
    session_maker = async_sessionmaker(
        engine, class_=AsyncSession, autoflush=False, expire_on_commit=False
    )
    async with session_maker() as session:
        yield session


async def add_many(data: ListApplicantsSchema) -> None:
    async with get_session() as session:
        session.add_all(data.to_database())
        await session.commit()
