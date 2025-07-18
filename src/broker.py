from faststream.kafka import KafkaBroker

from .database.session import add_many
from .schemas import ListApplicantsSchema

broker = KafkaBroker()


@broker.subscriber(
    "save_applicants",
    batch=True,
    batch_timeout_ms=1000,
    max_poll_records=1000,
)
async def save_applicants(data: ListApplicantsSchema) -> None:
    await add_many(data=data)
