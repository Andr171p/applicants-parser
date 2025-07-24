import asyncio
from datetime import datetime

from faststream import FastStream
from faststream.rabbit import RabbitBroker

from core import ApplicantSchema, DirectionSchema, EducationForm, Source, Submit, UniversitySchema
from database import add_all_applicants, add_directions, add_universitys
from settings import settings

broker = RabbitBroker(settings.rabbit_settings.get_rabbit_url)
app = FastStream(broker)


@broker.subscriber("universities")
async def save_universities(schema: UniversitySchema) -> None:
    await add_universitys(schema)


@broker.subscriber("directions")
async def save_directions(schema: DirectionSchema) -> None:
    await add_directions(schema)


@broker.subscriber("applicants")
async def save_applicants(data: list[ApplicantSchema]) -> None:
    await add_all_applicants(data)


@app.on_startup
async def start_app() -> None:
    await broker.connect()

    test_universitys = UniversitySchema(
        id=1314124,
        title="bdfbfbafdbaf",
        source=Source.GOSUSLUGI,
        url="jdfdfjbknjbdfkjkbdfjk",
    )
    test_directions = DirectionSchema(
        university_id=5445453,
        code="jbdfjdfbjkbdf",
        title="bkdfjnjfbdkjkbfd",
        education_form=EducationForm.EXTRAMURAL,
        institute="jgndfjndfgkjdf",
        budget_places=1,
        total_places=300,
        education_price=42141.1241,
    )
    test_applicants = [
        ApplicantSchema(
            university_id=2342423,
            direction_code="jkndfkfdkjf",
            id=13,
            serial_number=6466,
            priority=1,
            submit=Submit.NOT_SUBMITTED,
            total_points=240,
            points=[30, 90, 60],
            additional_points=10,
            original=False,
            status="gdfs",
            date=datetime.now(tz=None),
        ),
        ApplicantSchema(
            university_id=2342423,
            direction_code="jkndfkfdkjf",
            id=14,
            serial_number=6466,
            priority=1,
            submit=Submit.NOT_SUBMITTED,
            total_points=240,
            points=[30, 90, 60],
            additional_points=10,
            original=False,
            status="gdfs",
            date=datetime.now(tz=None),
        ),
        ApplicantSchema(
            university_id=2342423,
            direction_code="jkndfkfdkjf",
            id=15,
            serial_number=6466,
            priority=1,
            submit=Submit.NOT_SUBMITTED,
            total_points=240,
            points=[30, 90, 60],
            additional_points=10,
            original=False,
            status="gdfs",
            date=datetime.now(tz=None),
        ),
        ApplicantSchema(
            university_id=2342423,
            direction_code="jkndfkfdkjf",
            id=16,
            serial_number=6466,
            priority=1,
            submit=Submit.NOT_SUBMITTED,
            total_points=240,
            points=[30, 90, 60],
            additional_points=10,
            original=False,
            status="gdfs",
            date=datetime.now(tz=None),
        ),
    ]
    await broker.publish(message=test_universitys, queue="universitys")
    await broker.publish(message=test_directions, queue="directions")
    await broker.publish(message=test_applicants, queue="applicants")


@app.on_shutdown
async def stop_app() -> None:
    await broker.stop()


if __name__ == "__main__":
    asyncio.run(app.run())
