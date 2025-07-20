import asyncio
import logging

from playwright.async_api import async_playwright

from src.applicants_parser.browser.utils import aget_current_page
from src.applicants_parser.core.enums import EducationForm
from src.applicants_parser.parsers.gosuslugi.utils import (
    filter_directions,
    parse_direction,
    search_universities,
)


async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        urls = await search_universities(browser, query="ТюмГУ")
        page = await aget_current_page(browser)
        await page.goto(urls[2])
        urls = await filter_directions(
            browser=browser,
            education_forms=[EducationForm.FULL_TIME],
            education_levels=["Бакалавриат"],
        )
        direction = await parse_direction(browser, urls[10])
        print(direction)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
