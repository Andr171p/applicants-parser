from faststream import FastStream
from faststream.rabbit import RabbitBroker

from core import DirectionSchema, ListApplicantsSchema, UniversitySchema
from database import add_all_applicants, add_directions, add_universitys
from settings import settings

broker = RabbitBroker(settings.rabbit_settings.get_rabbit_url)
app = FastStream(broker)


@broker.subscriber("save_universitys")
async def save_universitys(schema: UniversitySchema) -> None:
    await add_universitys(schema)


@broker.subscriber("save_directions")
async def save_directions(schema: DirectionSchema) -> None:
    await add_directions(schema)


@broker.subscriber("save_applicants")
async def save_applicants(schema: ListApplicantsSchema) -> None:
    await add_all_applicants(schema)


@app.on_startup
async def start_app() -> None:
    await broker.connect()


@app.on_shutdown
async def stop_app() -> None:
    await broker.stop()
