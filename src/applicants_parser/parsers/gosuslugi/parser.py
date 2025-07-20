from playwright.async_api import async_playwright


class GosuslugiParser:
    def __init__(self, headless: bool = False) -> None:
        self.headless = headless

    async def parse(self) -> ...:
        async with async_playwright() as playwright:
            await playwright.chromium.launch(headless=self.headless)
