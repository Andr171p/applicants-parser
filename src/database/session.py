from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from ..core import ApplicantSchema, DirectionSchema, UniversitySchema
from ..settings import settings
from .models import ApplicantsModel, DirectionsModel, UniversitiesModel

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


async def add_universities(schema: UniversitySchema) -> None:
    async with get_session() as session:
        stmt = insert(UniversitiesModel).values(**schema.model_dump())
        await session.execute(stmt)
        await session.commit()


async def add_directions(schema: DirectionSchema) -> None:
    async with get_session() as session:
        stmt = insert(DirectionsModel).values(**schema.model_dump())
        await session.execute(stmt)
        await session.commit()


async def add_all_applicants(data: list[ApplicantSchema]) -> None:
    async with get_session() as session:
        stmt = [ApplicantsModel(**applicant.model_dump()) for applicant in data]
        session.add_all(stmt)
        await session.commit()
