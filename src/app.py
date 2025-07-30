import logging
from contextlib import asynccontextmanager

from dishka.integrations.faststream import setup_dishka
from faststream import FastStream
from faststream.rabbit import RabbitBroker
from playwright.async_api import async_playwright

from .broker import router
from .core.enums import EducationForm
from .dependencies import container
from .gosuslugi.graphs import build_university_graph
from .gosuslugi.helpers import generate_university_urls

EDUCATION_LEVELS: list[str] = ["Бакалавриат", "Специалитет"]

logger = logging.getLogger(__name__)


async def create_faststream_app() -> FastStream:
    broker = await container.get(RabbitBroker)
    broker.include_router(router)
    app = FastStream(broker)
    setup_dishka(container=container, app=app, auto_inject=True)
    return app


@asynccontextmanager
async def start_broker() -> None:
    faststream_app = await create_faststream_app()
    await faststream_app.broker.start()
    logger.info("Broker started")
    yield
    await faststream_app.broker.stop()
    logger.info("Broker closed")


async def execute_gosuslugi_parser() -> None:
    broker = await container.get(RabbitBroker)
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        graph = build_university_graph(broker, browser)
        for university_url in generate_university_urls():
            try:
                response = await graph.ainvoke({
                    "university_url": university_url,
                    "education_forms": [EducationForm.FULL_TIME],
                    "education_levels": EDUCATION_LEVELS,
                })
                logger.info(
                    "Received response from graph for %s, response: %s", university_url, response
                )
            except Exception as e:
                logger.exception("Error while parse %s, error: %s", university_url, e)
