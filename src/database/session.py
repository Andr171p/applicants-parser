from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..core import DirectionSchema, ListApplicantsSchema, UniversitySchema
from ..settings import settings

engine = create_async_engine(url=settings.sql_settings.get_db_url, echo=True)
session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    async with session_maker() as session:
        yield session


async def add_universitys(schema: UniversitySchema) -> None:
    async with get_session() as session:
        session.add(schema.to_model)
        await session.commit()


async def add_directions(schema: DirectionSchema) -> None:
    async with get_session() as session:
        session.add(schema.to_model)
        await session.commit()


async def add_all_applicants(schema: ListApplicantsSchema) -> None:
    async with get_session() as session:
        session.add_all(schema.to_database())
        await session.commit()
