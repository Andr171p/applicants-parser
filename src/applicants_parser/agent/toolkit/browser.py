from typing import Any, Optional

from pydantic import BaseModel, Field, ConfigDict

from playwright.async_api import Playwright, async_playwright, BrowserContext, Page, Browser


class BrowserState(BaseModel):
    """Состояние браузера для передачи между инструментами."""

    url: Optional[str] = None
    page_source: Optional[str] = None
    page: Optional[Page] = None
    context: Optional[BrowserContext] = None
    browser: Optional[Browser] = None
    playwright: Optional[Playwright] = None
    metadata: dict[str, Any] = Field(default_factory=dict)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    async def __aenter__(self) -> "BrowserState":
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.context = await self.browser.new_context()
        self.page = await self.context.new_page()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
