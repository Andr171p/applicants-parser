import asyncio
from playwright.async_api import async_playwright, Playwright


async def run(playwright: Playwright) -> None:
    chromium = playwright.chromium
    browser = await chromium.launch(headless=False)
    page = await browser.new_page()
    await page.goto("https://playwright.dev/python/docs/api/class-browsertype")
    await asyncio.sleep(5)
    # other actions...
    await browser.close()


async def main() -> None:
    async with async_playwright() as playwright:
        await run(playwright)


asyncio.run(main())
