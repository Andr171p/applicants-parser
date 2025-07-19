import asyncio
import logging

from playwright.async_api import async_playwright

from src.applicants_parser.browser.utils import aget_current_page
from src.applicants_parser.core.enums import EducationForm
from src.applicants_parser.parsers.gosuslugi.utils import (
    afilter_directions,
    aget_directions,
    asearch_universities,
)


async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        urls = await asearch_universities(browser, query="ТюмГУ")
        page = await aget_current_page(browser)
        await page.goto(urls[2])
        await afilter_directions(
            browser=browser,
            education_forms=[EducationForm.FULL_TIME],
            education_levels=["Базовое высшее"],
        )
        directions = await aget_directions(browser)
        print(directions)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
