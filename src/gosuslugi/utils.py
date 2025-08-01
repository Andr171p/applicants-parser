from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser

import logging
from pathlib import Path

from ..browser.utils import aget_current_page, ascroll_to_click
from ..core.enums import EducationForm
from ..core.schemas import DirectionSchema
from .constants import (
    EDUCATION_LEVEL,
    GOSUSLUGI_SEARCH_URL,
    GOSUSLUGI_URL,
    TECHNICAL_ERROR,
    TIMEOUT,
)
from .helpers import extract_direction_code
from .selectors import (
    BUDGET_PLACES_XPATH,
    DOWNLOAD_AS_TABLE_SELECTOR,
    EDUCATION_FORM_FILTER_SELECTOR,
    EDUCATION_FORM_SELECTOR,
    EDUCATION_LEVEL_FILTER_SELECTOR,
    EDUCATION_PRICE_SELECTOR,
    EDUCATION_PROGRAM_SELECTOR,
    FETCH_PROFILE_SCRIPT,
    FILTER_BUTTON_SELECTOR,
    INSTITUTE_SELECTOR,
    LIST_OF_APPLICANTS_SELECTOR,
    ORGANIZATION_CARD_SELECTOR,
    RECEPTIONS_SELECTOR,
    SEE_MORE_BUTTON_SELECTOR,
    TOTAL_PLACES_SELECTOR,
)
from .validators import DirectionValidator

logger = logging.getLogger(__name__)


async def search_university_urls(browser: AsyncBrowser, query: str) -> list[str]:
    """Выполняет поиск университетов по запросу.

    :param browser: Асинхронный Playwright браузер.
    :param query: Запрос для поиска университета, например `МГУ`
    :return Список найденных URL адресов вузов.
    """
    logger.info("---SEARCH UNIVERSITIES BY QUERY `%s`---", query)
    page = await aget_current_page(browser)
    url = f"{GOSUSLUGI_SEARCH_URL}{query}"
    await page.goto(url)
    await page.wait_for_selector(f"//{ORGANIZATION_CARD_SELECTOR}", state="attached")
    university_cards = await page.query_selector_all(f"xpath=//{ORGANIZATION_CARD_SELECTOR}")
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
    button = await page.wait_for_selector(FILTER_BUTTON_SELECTOR, timeout=TIMEOUT * 2000)
    await button.click()
    for education_form in education_forms:
        await page.click(EDUCATION_FORM_FILTER_SELECTOR.format(education_form=education_form))
        logger.info("---CHOSEN EDUCATION FORM `%s`---", education_form.upper())
    for education_level in education_levels:
        await page.click(EDUCATION_LEVEL_FILTER_SELECTOR.format(education_level=education_level))
        logger.info("---CHOSEN EDUCATION LEVEL `%s`", education_level.upper())
    await page.click("button:has-text('Применить')")
    logger.info("---SUBMIT FILTERS---")
    return await parse_direction_urls(browser)


async def parse_direction_urls(browser: AsyncBrowser) -> list[str]:
    """Получает все URL адреса направлений подготовки на текущей странице.

    :param browser: Асинхронный экземпляр Playwright браузера.
    :return Список URL адресов направлений подготовки.
    """
    logger.info("---PARSE DIRECTION URLS---")
    page = await aget_current_page(browser)
    await page.wait_for_selector(EDUCATION_PROGRAM_SELECTOR)
    while True:
        is_clickable = await ascroll_to_click(page, SEE_MORE_BUTTON_SELECTOR)
        if not is_clickable:
            break
        logger.info("---SCROLLED FOR MORE DIRECTIONS---")
        await page.wait_for_timeout(TIMEOUT)
        await page.evaluate("window.scrollBy(0, 500)")
    direction_cards = await page.query_selector_all(EDUCATION_PROGRAM_SELECTOR)
    direction_urls: list[str] = []
    for direction_card in direction_cards:
        link = await direction_card.query_selector("a.education-program-card[href]")
        if link:
            link_href = await link.get_attribute("href")
            if link_href:
                direction_url = f"{GOSUSLUGI_URL}{link_href}"
                direction_urls.append(direction_url)
    logger.info("---PARSED %s DIRECTIONS URLS--", len(direction_urls))
    return direction_urls


async def parse_direction(browser: AsyncBrowser, url: str) -> DirectionSchema | None:
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
    profiles = await page.evaluate(FETCH_PROFILE_SCRIPT)
    direction_kwargs["name"] = profiles[0]
    await page.click("h4.title-h4")
    education_form = await page.query_selector(EDUCATION_FORM_SELECTOR)
    if education_form:
        direction_kwargs["education_form"] = await education_form.text_content()
    institute = await page.query_selector(INSTITUTE_SELECTOR)
    if institute:
        direction_kwargs["institute"] = (await institute.text_content()).strip()
    direction_kwargs["budget_places"] = await page.text_content(BUDGET_PLACES_XPATH)
    direction_kwargs["total_places"] = await page.text_content(TOTAL_PLACES_SELECTOR)
    direction_kwargs["education_price"] = await page.text_content(EDUCATION_PRICE_SELECTOR)
    return DirectionValidator(**direction_kwargs)


async def save_applicants(browser: AsyncBrowser, dir_path: str | Path) -> None:
    """Асинхронно сохраняет списки подавших документы в excel формате.

    :param browser: Асинхронный Playwright браузер.
    :param dir_path: Путь до директории в которую нужно сохранить конкурсный список.
    """
    logger.info("---SAVE APPLICANTS---")
    page = await aget_current_page(browser)
    await page.wait_for_selector(LIST_OF_APPLICANTS_SELECTOR, timeout=TIMEOUT)
    list_of_applicants = await page.query_selector(LIST_OF_APPLICANTS_SELECTOR)
    await list_of_applicants.click()
    await page.wait_for_selector(RECEPTIONS_SELECTOR, timeout=TIMEOUT)
    receptions = await page.query_selector_all(f"{RECEPTIONS_SELECTOR} li.list-divider")
    applicant_list_urls: list[str] = []
    for reception in receptions:
        link = await reception.query_selector("a.link-plain")
        if link:
            link_href = await link.get_attribute("href")
            applicant_list_urls.append(f"{GOSUSLUGI_URL}{link_href}")
    logger.info("---FOUND %s APPLICANT LISTS---", len(applicant_list_urls))
    paths: list[str] = []
    for applicant_list_url in applicant_list_urls:
        await page.goto(applicant_list_url)
        await page.wait_for_selector(DOWNLOAD_AS_TABLE_SELECTOR, timeout=TIMEOUT * 10)
        async with page.expect_download() as download:
            await page.click(DOWNLOAD_AS_TABLE_SELECTOR)
        downloaded = await download.value
        path = f"{dir_path}/{downloaded.suggested_filename}"
        await downloaded.save_as(path)
        paths.append(path)
        logger.info("---SUCCESSFULLY SAVED APPLICANTS LIST---")
        await page.go_back()
    return paths
