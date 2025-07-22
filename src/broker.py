from faststream import FastStream
from faststream.rabbit import RabbitBroker

from config import settings
from database import ListApplicantsSchema, add_many

broker = RabbitBroker(settings.rabbit_settings.get_rabbit_url)
app = FastStream(broker)


@broker.subscriber("save_applicants")
async def save_applicants(data: dict) -> None:
    applicants = ListApplicantsSchema(**data)
    await add_many(data=applicants)


@app.on_startup
async def start_app() -> None:
    await broker.connect()


@app.on_shutdown
async def stop_app() -> None:
    await broker.stop()
