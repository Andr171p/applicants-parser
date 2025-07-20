from __future__ import annotations

from typing import Any, TypedDict, TYPE_CHECKING

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser

from abc import ABC, abstractmethod
import logging

from ...browser.utils import aget_current_page
from ...core.schemas import University
from ...core.enums import Source
from .fsm import UniversityState, AdmissionListState
from .helpers import extract_direction_code
from .validators import DirectionValidator
from .utils import parse_direction_urls
from .constants import TIMEOUT, TECHNICAL_ERROR, GOSUSLUGI_URL
from .selectors import (
    ORGANIZATION_TITLE_SELECTOR,
    FILTER_BUTTON_SELECTOR,
    EDUCATION_FORM_FILTER_SELECTOR,
    EDUCATION_LEVEL_FILTER_SELECTOR,
    FETCH_PROFILE_SCRIPT,
    EDUCATION_FORM_SELECTOR,
    INSTITUTE_SELECTOR,
    BUDGET_PLACES_XPATH,
    TOTAL_PLACES_SELECTOR,
    EDUCATION_PRICE_SELECTOR,
    RECEPTIONS_SELECTOR,
    LIST_OF_APPLICANTS_SELECTOR,
    DOWNLOAD_AS_TABLE_SELECTOR
)

logger = logging.getLogger(__name__)


class BaseNode(ABC):
    def __init__(self, browser: AsyncBrowser) -> None:
        self.browser = browser

    @abstractmethod
    async def __call__(self, state: TypedDict) -> TypedDict: pass


class ParseUniversity(BaseNode):
    async def __call__(self, state: UniversityState) -> UniversityState:
        logger.info("---SELECT UNIVERSITY---")
        url = state["university_url"]
        page = await aget_current_page(self.browser)
        await page.goto(url)
        title = await page.locator(ORGANIZATION_TITLE_SELECTOR).text_content()
        university = University(
            id=url.split("/")[-1],
            title=title.strip(),
            source=Source.GOSUSLUGI,
            url=url
        )
        return {"university": university}


class FilterDirections(BaseNode):
    async def __call__(self, state: UniversityState) -> UniversityState:
        logger.info("---FILTER DIRECTIONS---")
        page = await aget_current_page(self.browser)
        button = await page.wait_for_selector(FILTER_BUTTON_SELECTOR, timeout=TIMEOUT)
        await button.click()
        for education_form in state["education_forms"]:
            await page.click(
                EDUCATION_FORM_FILTER_SELECTOR.format(education_form=education_form)
            )
            logger.info("---CHOSEN EDUCATION FORM `%s`---", education_form.upper())
        for education_level in state["education_levels"]:
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
        direction_kwargs["education_price"] = await page.text_content(
            EDUCATION_PRICE_SELECTOR
        )
        direction = DirectionValidator(**direction_kwargs)
        return {"direction": direction}


class DownloadApplicantLists(BaseNode):
    async def __call__(self, state: AdmissionListState) -> AdmissionListState:
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
            dir_path = state["dir_path"]
            admission_list_file = f"{dir_path}/{download_value.suggested_filename}"
            await download_value.save_as(admission_list_file)
            admission_list_files.append(admission_list_file)
            logger.info("---SUCCESSFULLY SAVED APPLICANTS LIST---")
            await page.go_back()
        return {"admission_list_files": admission_list_files}


class ParseApplicants(BaseNode):
    async def __call__(self, state: AdmissionListState) -> AdmissionListState:
        logger.info("---PARSE APPLICANTS---")
        ...


class SaveApplicantsLists(BaseNode):
    async def __call__(self, state: AdmissionListState) -> AdmissionListState:
        logger.info("---SAVE APPLICANTS LISTS---")
        ...
