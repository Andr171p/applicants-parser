from faststream.rabbit import RabbitRouter

from .core import ApplicantSchema, DirectionSchema, UniversitySchema
from .database import add_all_applicants, add_directions, add_universitys

router = RabbitRouter()


@router.subscriber("universities")
async def save_universities(schema: UniversitySchema) -> None:
    await add_universitys(schema)


@router.subscriber("directions")
async def save_directions(schema: DirectionSchema) -> None:
    await add_directions(schema)


@router.subscriber("applicants")
async def save_applicants(data: list[ApplicantSchema]) -> None:
    await add_all_applicants(data)
