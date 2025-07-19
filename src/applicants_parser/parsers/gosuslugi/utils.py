from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser

import logging

from ...browser.utils import aget_current_page, ascroll_to_click
from ...core.schemas import EducationForm
from .constants import EDUCATION_LEVEL, GOSUSLUGI_SEARCH_URL, GOSUSLUGI_URL, TIMEOUT

logger = logging.getLogger(__name__)


async def asearch_universities(browser: AsyncBrowser, query: str) -> list[str]:
    """Выполняет поиск университетов по запросу.

    :param browser: Асинхронный Playwright браузер.
    :param query: Запрос для поиска университета, наприер `МГУ`
    :return Список найденных URL адресов вузов.
    """
    logger.info("---SEARCH UNIVERSITIES BY QUERY `%s`---", query)
    css_selector = "app-organization-card"
    page = await aget_current_page(browser)
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
    logger.info("---FOUND %s UNIVERSITIES---", len(university_urls))
    return university_urls


async def afilter_directions(
    browser: AsyncBrowser,
    education_forms: list[EducationForm],
    education_levels: list[EDUCATION_LEVEL],
) -> None:
    """Асинхроно выполняет фильтрацию направлений подготовки вуза.

    :param browser: Экземпляр асинхронного Playwright браузера.
    :param education_forms: Список форм обучения по которым выполняется фильтрация.
    :param education_levels: Список уровней образования, например `Бакалавриат`.
    :return Страница с отфильтрованными направлениями подготовки.
    """
    logger.info("---FILTER DIRECTIONS---")
    page = await aget_current_page(browser)
    button = await page.wait_for_selector("button.filter-button", timeout=TIMEOUT * 2000)
    await button.click()
    for education_form in education_forms:
        css_selector = (
            f"form[formgroupname='educationForms'] div.text-plain:has-text('{education_form}')"
        )
        await page.click(css_selector)
        logger.info("---CHOOSEN EDUCATION FORM `%s`---", education_form.upper())
    for education_level in education_levels:
        css_selector = (
            f"form[formgroupname='educationLevels'] div.text-plain:has-text('{education_level}')"
        )
        await page.click(css_selector)
        logger.info("---CHOOSEN EDUCATION LEVEL `%s`", education_level.upper())
    await page.click("button:has-text('Применить')")
    logger.info("---SUBMIT FILTERS---")


async def aget_directions(browser: AsyncBrowser) -> list[str]:
    direction_css_selector = "app-education-program-card"
    button_css_selector = "button.white.button:has-text('Посмотреть ещё')"
    page = await aget_current_page(browser)
    await page.wait_for_selector(direction_css_selector)
    while True:
        is_clickable = await ascroll_to_click(page, button_css_selector)
        if not is_clickable:
            break
        await page.wait_for_timeout(TIMEOUT)
        await page.evaluate("window.scrollBy(0, 500)")
    direction_cards = await page.query_selector_all(direction_css_selector)
    direction_urls: list[str] = []
    for direction_card in direction_cards:
        link = await direction_card.query_selector("a.education-program-card[href]")
        if link:
            link_href = await link.get_attribute("href")
            if link_href:
                direction_url = f"{GOSUSLUGI_URL}{link_href}"
                direction_urls.append(direction_url)
    return direction_urls
