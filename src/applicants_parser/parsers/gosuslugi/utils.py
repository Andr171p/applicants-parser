from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser

import logging

from ...browser.utils import aget_current_page
from ...constants import GOSUSLUGI_SEARCH_URL, GOSUSLUGI_URL

logger = logging.getLogger(__name__)


async def asearch_universities(async_browser: AsyncBrowser, query: str) -> list[str]:
    logger.info(f"---SEARCH UNIVERSITIES BY QUERY {query}---")  # noqa: G004
    css_selector = "app-organization-card"
    page = await aget_current_page(async_browser)
    url = f"{GOSUSLUGI_SEARCH_URL}{query}"
    await page.goto(url)
    await page.wait_for_selector(f"//{css_selector}", state="attached")
    university_cards = await page.query_selector_all(f"xpath=//{css_selector}")
    university_urls: list[str] = []
    for university_card in university_cards:
        link = await university_card.query_selector("xpath=.//a")
        link_href = await link.get_attribute("href") if link else "#"
        university_url = f"{GOSUSLUGI_URL}{link_href}"
        university_urls.append(university_url)
    logger.info(f"---FOUND {len(university_urls)} UNIVERSITIES---")  # noqa: G004
    return university_urls


async def afilter_directions(async_browser: AsyncBrowser) -> ...:
    logger.info("---FILTER DIRECTIONS---")
