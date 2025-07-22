from __future__ import annotations

import json
import logging
from collections.abc import Sequence
from urllib.parse import urlparse

from langchain_core.callbacks import AsyncCallbackManagerForToolRun, CallbackManagerForToolRun
from langchain_core.tools import ArgsSchema
from pydantic import BaseModel, Field, field_validator, model_validator

from ..browser.helpers import clean_html
from ..browser.tool import BaseBrowserTool
from ..browser.utils import (
    ATTRIBUTE,
    aget_current_page,
    aget_elements,
    get_current_page,
    get_elements,
)

logger = logging.getLogger(__name__)

TIMEOUT = 1_000
PROTOCOLS: tuple[str, str] = ("http", "https")


class ClickArgsSchema(BaseModel):
    css_selector: str = Field(..., description="CSS селектор элемента на который нужно нажать.")


class ClickTool(BaseBrowserTool):
    name: str = "click_element"
    description: str = "Нажимает кнопку на веб-странице по CSS-селектору."
    args_schema: ArgsSchema | None = ClickArgsSchema

    visible_only: bool = (
        True  # True для нажатия только видимых элементов, False для всех остальных.
    )
    strict_mode: bool = (
        False  # Строгий режим, требует нахождения только одного CSS селектора на странице.
    )
    timeout: float = TIMEOUT  # Время для ожидания загрузки элемента.

    def _css_selector_effective(self, css_selector: str) -> str:
        if self.visible_only:
            return css_selector
        return f"{css_selector} >> visible=1"

    def _run(self, css_selector: str, run_manager: CallbackManagerForToolRun | None = None) -> str:  # noqa: ARG002
        logger.info("---CLICK ELEMENT---")

        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError  # noqa: PLC0415

        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        css_selector_effective = self._css_selector_effective(css_selector)
        try:
            page.click(css_selector_effective, strict=self.strict_mode, timeout=self.timeout)
        except PlaywrightTimeoutError:
            return f"Не получилось нажать на элемент: '{css_selector}'"
        return f"Нажат элемент: '{css_selector}'"

    async def _arun(
        self,
        css_selector: str,
        run_manager: AsyncCallbackManagerForToolRun | None = None,  # noqa: ARG002
    ) -> str:
        logger.info("---CLICK ELEMENT---")

        from playwright.async_api import TimeoutError as PlaywrightTimeoutError  # noqa: PLC0415

        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        css_selector_effective = self._selector_effective(css_selector)
        try:
            await page.click(css_selector_effective, strict=self.strict_mode, timeout=self.timeout)
        except PlaywrightTimeoutError:
            return f"Не получилось нажать на элемент: '{css_selector}'"
        return f"Нажат элемент: '{css_selector}'"


class CurrentURLTool(BaseBrowserTool):
    name: str = "current_url"
    description: str = "Получает URL адрес текущей страницы."

    def _run(
        self,
        run_manager: CallbackManagerForToolRun | None = None,  # noqa: ARG002
    ) -> str:
        logger.info("---GET CURRENT PAGE URL---")
        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        return page.url

    async def _arun(
        self,
        run_manager: AsyncCallbackManagerForToolRun | None = None,  # noqa: ARG002
    ) -> str:
        logger.info("---GET CURRENT PAGE URL---")
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        return page.url


class ExtractTextTool(BaseBrowserTool):
    name: str = "extract_text"
    description: str = "Извлекает весь текст с текущей страницы."

    @model_validator(mode="before")
    def check_bs4_importing(self) -> ExtractTextTool:
        """Проверяет установлен ли bs4"""
        try:
            from bs4 import BeautifulSoup  # noqa: F401, PLC0415
        except ImportError:
            raise ImportError(  # noqa: B904
                "The 'beautifulsoup4' package is required to use this tool."
                " Please install it with 'pip install beautifulsoup4'."
            )
        return self

    def _run(self, run_manager: CallbackManagerForToolRun | None = None) -> str:  # noqa: ARG002
        logger.info("---EXTRACT TEXT---")

        from bs4 import BeautifulSoup  # noqa: PLC0415

        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        html_content = page.content()
        soup = BeautifulSoup(html_content, "lxml")
        return " ".join(text for text in soup.stripped_strings)

    async def _arun(self, run_manager: AsyncCallbackManagerForToolRun | None = None) -> str:  # noqa: ARG002
        logger.info("---EXTRACT TEXT---")

        from bs4 import BeautifulSoup  # noqa: PLC0415

        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        html_content = await page.content()
        soup = BeautifulSoup(html_content, "lxml")
        return " ".join(text for text in soup.stripped_strings)


class ExtractHTMLTool(BaseBrowserTool):
    name: str = "extract_html"
    description = "Извлекает HTML код страницы."

    def _run(self, run_manager: CallbackManagerForToolRun | None = None) -> str:  # noqa: ARG002
        logger.info("---EXTRACT HTML---")
        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        html_content = page.content()
        return clean_html(html_content)

    async def _arun(self, run_manager: AsyncCallbackManagerForToolRun | None = None) -> str:  # noqa: ARG002
        logger.info("---EXTRACT HTML---")
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        html_content = await page.content()
        return clean_html(html_content)


class RetrieveElementsArgsSchema(BaseModel):
    css_selector: str = Field(
        ..., description="CSS селектор, например: '*', 'div', 'p', 'a', #id, .classname"
    )
    attributes: list[str] = Field(
        default_factory=lambda: ["innerText"],
        description="Набора атрибутов, которые необходимо получить для каждого элемента.",
    )


class ExtractHyperLinksTool(BaseBrowserTool): ...


class RetrieveElementsTool(BaseBrowserTool):
    name: str = "retrieve_elements"
    description: str = (
        "Получает элементы на текущей станице, соответствующие заданному CSS селектору."
    )
    args_schema: ArgsSchema | None = RetrieveElementsArgsSchema

    def _run(
        self,
        css_selector: str,
        attributes: Sequence[str] = ATTRIBUTE,
        run_manager: CallbackManagerForToolRun | None = None,
    ) -> str:
        logger.info("---RETRIEVE ELEMENTS---")
        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        results = get_elements(page, css_selector, attributes)
        return json.dumps(results, ensure_ascii=False)

    async def _arun(
        self,
        css_selector: str,
        attributes: Sequence[str] = ATTRIBUTE,
        run_manager: AsyncCallbackManagerForToolRun | None = None,
    ) -> str:
        logger.info("---RETRIEVE ELEMENTS---")
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        results = await aget_elements(page, css_selector, attributes)
        return json.dumps(results, ensure_ascii=False)


class NavigationArgsSchema(BaseModel):
    url: str = Field(..., description="URL по которому нужно перейти.")

    @field_validator("url", mode="before")
    def validate_url(cls, url: str) -> str:
        """Проверяет валиден ли URL"""
        parsed_url = urlparse(url)
        if parsed_url.scheme not in PROTOCOLS:
            raise ValueError(f"URL scheme must be {PROTOCOLS}")
        return url


class NavigationTool(BaseBrowserTool):
    name: str = "navigation"
    description: str = "Переходит по указанному URL"
    args_schema: ArgsSchema | None = NavigationArgsSchema

    def _run(self, url: str, run_manager: CallbackManagerForToolRun | None = None) -> str:  # noqa: ARG002
        logger.info("---NAVIGATE TO %s---", url)
        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        response = page.goto(url)
        status = response.status if response else "unknown"
        return f"Переход по {url}, status code: {status}"

    async def _arun(
        self, url: str, run_manager: AsyncCallbackManagerForToolRun | None = None  # noqa: ARG002
    ) -> str:
        logger.info("---NAVIGATE TO %s---", url)
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        response = await page.goto(url)
        status = response.status if response else "unknown"
        return f"Переход по {url}, status code: {status}"


class NavigateBackTool(BaseBrowserTool):
    name: str = "navigate_back"
    description: str = "Переходит на предыдущую web-страницу в истории браузера."

    def _run(self, run_manager: CallbackManagerForToolRun | None = None) -> str:  # noqa: ARG002
        logger.info("---NAVIGATE BACK---")
        if self.sync_browser is None:
            raise ValueError(f"Synchronous browser not provided to {self.name}")
        page = get_current_page(self.sync_browser)
        response = page.go_back()
        if response:
            return (
                f"Переход на предыдущую страницу по URL адресу: '{response.url}'."
                f" Status code: {response.status}"
            )
        return "Невозможно вернуться назад; нет предыдущей страницы в истории"

    async def _arun(self, run_manager: AsyncCallbackManagerForToolRun | None = None) -> str:  # noqa: ARG002
        logger.info("---NAVIGATE BACK---")
        if self.async_browser is None:
            raise ValueError(f"Asynchronous browser not provided to {self.name}")
        page = await aget_current_page(self.async_browser)
        response = await page.go_back()
        if response:
            return (
                f"Переход на предыдущую страницу по URL адресу: '{response.url}'."
                f" Status code: {response.status}"
            )
        return "Невозможно вернуться назад; нет предыдущей страницы в истории"
