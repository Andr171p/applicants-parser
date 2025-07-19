import asyncio
import logging

from playwright.async_api import async_playwright

from src.applicants_parser.browser.utils import aget_current_page
from src.applicants_parser.core.enums import EducationForm
from src.applicants_parser.parsers.gosuslugi.utils import (
    afilter_direction_urls,
    aparse_direction,
    asearch_university_urls,
)


async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        urls = await asearch_university_urls(browser, query="ТюмГУ")
        page = await aget_current_page(browser)
        await page.goto(urls[2])
        urls = await afilter_direction_urls(
            browser=browser,
            education_forms=[EducationForm.FULL_TIME],
            education_levels=["Бакалавриат"],
        )
        direction = await aparse_direction(browser, urls[0])
        print(direction)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
