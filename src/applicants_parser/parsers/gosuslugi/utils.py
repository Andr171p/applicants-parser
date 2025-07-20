from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser

import logging

from ...browser.utils import aget_current_page, ascroll_to_click
from ...core.enums import EducationForm
from ...core.schemas import Direction
from .constants import EDUCATION_LEVEL, GOSUSLUGI_SEARCH_URL, GOSUSLUGI_URL, TIMEOUT
from .helpers import extract_direction_code
from .validators import DirectionValidator

TECHNICAL_ERROR = "Техническая ошибка"

logger = logging.getLogger(__name__)


async def search_universities(browser: AsyncBrowser, query: str) -> list[str]:
    """Выполняет поиск университетов по запросу.

    :param browser: Асинхронный Playwright браузер.
    :param query: Запрос для поиска университета, например `МГУ`
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


async def filter_directions(
    browser: AsyncBrowser,
    education_forms: list[EducationForm],
    education_levels: list[EDUCATION_LEVEL],
) -> list[str]:
    """Асинхронно выполняет фильтрацию направлений подготовки вуза.

    :param browser: Экземпляр асинхронного Playwright браузера.
    :param education_forms: Список форм обучения по которым выполняется фильтрация.
    :param education_levels: Список уровней образования, например `Бакалавриат`.
    :return Список URL адресов отфильтрованных направлений подготовки.
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
        logger.info("---CHOSEN EDUCATION FORM `%s`---", education_form.upper())
    for education_level in education_levels:
        css_selector = (
            f"form[formgroupname='educationLevels'] div.text-plain:has-text('{education_level}')"
        )
        await page.click(css_selector)
        logger.info("---CHOSEN EDUCATION LEVEL `%s`", education_level.upper())
    await page.click("button:has-text('Применить')")
    logger.info("---SUBMIT FILTERS---")
    return await get_direction_urls(browser)


async def get_direction_urls(browser: AsyncBrowser) -> list[str]:
    """Получает все URL адреса направлений подготовки на текущей странице.

    :param browser: Асинхронный экземпляр Playwright браузера.
    :return Список URL адресов направлений подготовки.
    """
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


async def parse_direction(browser: AsyncBrowser, url: str) -> Direction | None:
    """Асинхронно парсит направление подготовки.

    :param browser: Экземпляр асинхронного Playwright браузера.
    :param url: URL адрес направления подготовки.
    :return: Pydantic схема направления подготовки.
    """
    logger.info("---PARSE DIRECTION %s---", url)
    direction_kwargs: dict[str, Any] = {}
    page = await aget_current_page(browser)
    await page.goto(url)
    element = await page.query_selector("div.text-center")
    if element is not None and element.inner_text() == TECHNICAL_ERROR:
        await page.go_back()
        return None
    await page.wait_for_selector("h4.title-h4")
    direction_kwargs["university_id"] = url.split("/")[-1]  # noqa: PLC0207
    direction_kwargs["code"] = extract_direction_code(url)
    profiles = await page.evaluate("""() => {
        return Array.from(document.querySelectorAll('lib-expansion-panel'))
            .map(el => {
                const root = el.shadowRoot || el;
                const title = root.querySelector('h4.title-h4');
                return title ? title.textContent.trim() : null;
            })
            .filter(Boolean);
    }""")
    print(profiles)
    direction_kwargs["name"] = profiles[0]
    await page.click("h4.title-h4")
    education_form = await page.query_selector(
        "div.small-text.gray:has-text('Форма обучения') + div.text-plain"
    )
    if education_form:
        direction_kwargs["education_form"] = await education_form.text_content()
    institute = await page.query_selector("div.text-plain.mb-24.ng-star-inserted")
    if institute:
        direction_kwargs["institute"] = (await institute.text_content()).strip()
    direction_kwargs["budget_places"] = await page.text_content(
        "xpath=//li[.//div[contains(@class, 'gray') and text()='Основные места']]"
        "//div[contains(@class, 'bold')]"
    )
    total_places = await page.text_content("div.header-places div.small-text")
    direction_kwargs["total_places"] = total_places.replace(" ", "").replace("&nbsp;", "")
    direction_kwargs["education_price"] = await page.text_content("div.title-h3.mb-8")
    print(direction_kwargs)
    return DirectionValidator(**direction_kwargs)
