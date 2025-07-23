from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser

import asyncio
import logging
import os
from abc import ABC, abstractmethod

import polars as pl
from playwright.async_api import TimeoutError as PlaywrightTimeoutError

from ..browser.utils import aget_current_page
from ..core.base import Broker
from ..core.enums import Source
from ..core.schemas import ApplicantSchema, UniversitySchema
from ..settings import ADMISSION_LISTS_DIR
from .constants import GOSUSLUGI_URL, TECHNICAL_ERROR, TIMEOUT, ZERO_VALUE
from .helpers import extract_direction_code, extract_university_id, format_row
from .selectors import (
    BUDGET_PLACES_XPATH,
    DOWNLOAD_AS_TABLE_SELECTOR,
    EDUCATION_FORM_FILTER_SELECTOR,
    EDUCATION_FORM_SELECTOR,
    EDUCATION_LEVEL_FILTER_SELECTOR,
    EDUCATION_PRICE_SELECTOR,
    FETCH_PROFILE_SCRIPT,
    FILTER_BUTTON_SELECTOR,
    INSTITUTE_SELECTOR,
    LIST_OF_APPLICANTS_SELECTOR,
    ORGANIZATION_TITLE_SELECTOR,
    RECEPTIONS_SELECTOR,
    TOTAL_PLACES_SELECTOR,
)
from .states import AdmissionListState, UniversityState
from .utils import parse_direction_urls
from .validators import ApplicantValidator, DirectionValidator

logger = logging.getLogger(__name__)


class BaseNode(ABC):
    """Базовый класс для создания узла (вершины графа)."""
    def __init__(self, browser: AsyncBrowser) -> None:
        self.browser = browser

    @abstractmethod
    async def __call__(self, state: dict[str, Any]) -> dict[str, Any]: pass


class ParseUniversity(BaseNode):
    """Парсинг информации об университете по его URL с Госуслуг."""
    async def __call__(self, state: UniversityState) -> UniversityState:
        logger.info("---SELECT UNIVERSITY---")
        url = state["university_url"]
        page = await aget_current_page(self.browser)
        await page.goto(url)
        title = await page.locator(ORGANIZATION_TITLE_SELECTOR).text_content()
        university = UniversitySchema(
            id=extract_university_id(url),
            title=title.strip(),
            source=Source.GOSUSLUGI,
            url=url
        )
        return {"university": university}


class FilterDirectionURLs(BaseNode):
    """Фильтрация направлений подготовки на странице."""
    async def __call__(self, state: UniversityState) -> UniversityState:
        logger.info("---FILTER DIRECTIONS---")
        page = await aget_current_page(self.browser)
        button = await page.wait_for_selector(FILTER_BUTTON_SELECTOR, timeout=TIMEOUT)
        await button.click()
        for education_form in state.get("education_forms", []):
            await page.click(
                EDUCATION_FORM_FILTER_SELECTOR.format(education_form=education_form)
            )
            logger.info("---CHOSEN EDUCATION FORM `%s`---", education_form.upper())
        for education_level in state.get("education_levels", []):
            await page.click(
                EDUCATION_LEVEL_FILTER_SELECTOR.format(
                    education_level=education_level)
            )
            logger.info("---CHOSEN EDUCATION LEVEL `%s`", education_level.upper())
        await page.click("button:has-text('Применить')")
        logger.info("---SUBMIT FILTERS---")
        direction_urls = await parse_direction_urls(self.browser)
        return {"direction_urls": direction_urls}


class ParseDirection(BaseNode):
    """Парсинг конкретного направления подготовки."""
    async def __call__(self, state: AdmissionListState) -> AdmissionListState:
        url = state["direction_url"]
        logger.info("---PARSE DIRECTION %s---", url)
        direction_kwargs: dict[str, Any] = {}
        page = await aget_current_page(self.browser)
        await page.goto(url)
        element = await page.query_selector("div.text-center")
        if element is not None and element.inner_text() == TECHNICAL_ERROR:
            await page.go_back()
            return None
        await page.wait_for_selector("h4.title-h4")
        direction_kwargs["university_id"] = url.split("/")[-1]
        direction_kwargs["code"] = extract_direction_code(url)
        profiles = await page.evaluate(FETCH_PROFILE_SCRIPT)
        direction_kwargs["title"] = profiles[0]
        await page.click("h4.title-h4")
        education_form = await page.query_selector(EDUCATION_FORM_SELECTOR)
        if education_form:
            direction_kwargs["education_form"] = await education_form.text_content()
        institute = await page.query_selector(INSTITUTE_SELECTOR)
        if institute:
            direction_kwargs["institute"] = (await institute.text_content()).strip()
        try:
            direction_kwargs["budget_places"] = await page.text_content(
                BUDGET_PLACES_XPATH, timeout=TIMEOUT * 5
            )
        except PlaywrightTimeoutError:
            direction_kwargs["budget_places"] = ZERO_VALUE
        direction_kwargs["total_places"] = await page.text_content(TOTAL_PLACES_SELECTOR)
        direction_kwargs["education_price"] = await page.text_content(
            EDUCATION_PRICE_SELECTOR
        )
        direction = DirectionValidator(**direction_kwargs)
        return {"direction": direction}


class DownloadApplicants(BaseNode):
    """Скачивание файлов с конкурсными списками."""
    async def __call__(
        self, state: AdmissionListState  # noqa: ARG002
) -> AdmissionListState:
        logger.info("---DOWNLOAD APPLICANTS LISTS---")
        page = await aget_current_page(self.browser)
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
        admission_list_files: list[str] = []
        for applicant_list_url in applicant_list_urls:
            await page.goto(applicant_list_url)
            await page.wait_for_selector(DOWNLOAD_AS_TABLE_SELECTOR, timeout=TIMEOUT * 10)
            async with page.expect_download() as download:
                await page.click(DOWNLOAD_AS_TABLE_SELECTOR)
            download_value = await download.value
            admission_list_file = f"{ADMISSION_LISTS_DIR}/{download_value.suggested_filename}"
            await download_value.save_as(admission_list_file)
            admission_list_files.append(admission_list_file)
            logger.info("---SUCCESSFULLY SAVED APPLICANTS LIST---")
            await page.go_back()
        return {"admission_list_files": admission_list_files}


class ParseApplicants(BaseNode):
    """Парсинг абитуриентов из файлов с конкурсными списками."""
    async def __call__(self, state: AdmissionListState) -> AdmissionListState:
        logger.info("---PARSE APPLICANTS---")
        applicants: list[ApplicantSchema] = []
        for admission_list_file in state.get("admission_list_files", []):
            try:
                df = pl.read_csv(admission_list_file)
                reception_applicants = [
                    ApplicantValidator.from_csv_row(
                        format_row(row),
                        university_id=state["university_id"],
                        direction_code=state["direction_url"]
                    )
                    for row in df.iter_rows()
                ]
                os.remove(admission_list_file)
                applicants.extend(reception_applicants)
                logger.info("---SUCCESSFULLY PARSED %s APPLICANTS---", len(applicants))
            except Exception as e:
                logger.exception("---ERROR OCCURRED %s---", e)  # noqa: TRY401
        return {"applicants": applicants}


class ParseAdmissionLists(BaseNode):
    """Парсинг всей информации об университете и конкурсных списков
    с отправкой в брокер сообщений.
    """
    def __init__(self, broker: Broker, browser: AsyncBrowser) -> None:
        super().__init__(browser)
        self.broker = broker

    async def __call__(self, state: UniversityState) -> UniversityState:
        from .graphs import build_admission_list_graph  # noqa: PLC0415

        logger.info("---START PARSE UNIVERSITY ADMISSION LISTS---")
        graph = build_admission_list_graph(self.browser)
        university_id = extract_university_id(state["university_url"])
        await self.broker.publish(state["university"], queue="universities")
        for direction_url in state.get("direction_urls", []):
            try:
                response = await graph.ainvoke({
                    "university_id": university_id,
                    "direction_url": direction_url
                })
                await asyncio.gather(
                    self.broker.publish(response.get("direction"), queue="directions"),
                    self.broker.publish(response.get("applicants"), queue="applicants")
                )
            except Exception as e:
                logger.exception("---ERROR OCCURRED %s---", e)  # noqa: TRY401
        return {"message": "FINISH"}
