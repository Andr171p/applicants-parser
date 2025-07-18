import asyncio
import logging

from playwright.async_api import async_playwright

from src.applicants_parser.parsers.gosuslugi.utils import asearch_universities


async def main() -> None:
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        urls = await asearch_universities(browser, query="ТюмГУ")
        print(urls)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
