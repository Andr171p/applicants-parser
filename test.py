import asyncio
import logging

from playwright.async_api import async_playwright
from pydantic import BaseModel

from src.core.enums import EducationForm
from src.gosuslugi.graphs import build_university_graph


class TestBroker:
    async def publish(
        self, messages: BaseModel | list[BaseModel] | list[dict] | dict | str, **kwargs
    ) -> None:
        print(f"Publish message to {kwargs.get('queue')}")


async def main() -> None:
    broker = TestBroker()
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        graph = build_university_graph(broker, browser)
        response = await graph.ainvoke({
            "university_url": "https://www.gosuslugi.ru/vuznavigator/universities/52",
            "education_forms": [EducationForm.FULL_TIME],
            "education_levels": ["Бакалавриат", "Специалитет"],
        })
        print(response)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
