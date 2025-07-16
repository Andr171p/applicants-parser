from typing import Optional, Literal

import asyncio
import logging

from pydantic import BaseModel, Field

from langchain_core.tools.base import ArgsSchema
from langchain_core.tools import BaseTool, ToolException
from langchain_core.language_models import BaseChatModel

from ..browser import BrowserState, clean_html

from .utils import create_structured_output_llm_chain
from .prompts import SEARCH_ELEMENT_PROMPT

TIMEOUT = 1

logger = logging.getLogger(__name__)


class OpenURLArgsSchema(BaseModel):
    url: str = Field(description="URL сайта или страницы.")


class OpenURLTool(BaseTool):
    name: str = "OpenURL"
    description: str = "Открывает сайт или ссылку по URL и получает её HTML разметку."
    args_schema: Optional[ArgsSchema] = OpenURLArgsSchema

    def __init__(self, browser_state: BrowserState, **kwargs) -> None:
        super().__init__(**kwargs)
        self._browser_state = browser_state

    def _run(self, url: str) -> str:
        raise NotImplementedError

    async def _arun(self, url: str) -> str:
        logger.info("---OPEN URL %s---", url)
        await self._browser_state.page.goto(url)
        await asyncio.sleep(TIMEOUT)
        self._browser_state.url = url
        page_source = await self._browser_state.page.content()
        self._browser_state.page_source = page_source
        return clean_html(page_source)


class NavigationArgsSchema(BaseModel):
    direction: Literal["back", "forward"] = Field(
        description="'back' - предыдущая страница, 'forward' - следующая страница."
    )


class NavigationTool(BaseTool):
    name: str = "Navigation"
    description: str = "Навигация между страницами в истории браузера."
    args_schema: Optional[ArgsSchema] = NavigationArgsSchema

    def __init__(self, browser_state: BrowserState, **kwargs) -> None:
        super().__init__(**kwargs)
        self._browser_state = browser_state

    def _run(self, direction: Literal["back", "forward"]) -> str:
        raise NotImplementedError

    async def _arun(self, direction: Literal["back", "forward"]) -> str:
        logger.info("---NAVIGATE %s---", direction.upper())
        if direction == "back":
            await self._browser_state.page.go_back()
        elif direction == "forward":
            await self._browser_state.page.go_forward()
        else:
            raise ToolException(f"Unsupported direction {direction}")
        await self._browser_state.page.wait_for_load_state()
        page_source = await self.browser_state.page.content()
        self._browser_state.page_source = page_source
        return clean_html(page_source)


class ClickButtonArgsSchema(BaseModel):
    css_selector: Optional[str] = Field(description="CSS селектор.")
    button_text: Optional[str] = Field(description="Текст кнопки.")


class ClickButtonTool(BaseTool):
    name: str = "ClickButton"
    description: str = """Нажимает кнопку на веб-странице по CSS-селектору или тексту кнопки.
        Возвращает HTML новой страницы после клика."""
    args_schema: Optional[ArgsSchema] = ClickButtonArgsSchema

    def __init__(self, browser_state: BrowserState, **kwargs) -> None:
        super().__init__(**kwargs)
        self._browser_state = browser_state

    def _run(self, css_selector: Optional[str] = None, button_text: Optional[str] = None) -> str:
        raise NotImplementedError

    async def _arun(
            self,
            css_selector: Optional[str] = None,
            button_text: Optional[str] = None
    ) -> str:
        logger.info("---CLICK BUTTON---")
        try:
            if css_selector:
                button = self._browser_state.page.locator(css_selector)
            elif button_text:
                button = self._browser_state.page.get_by_text(button_text)
            else:
                raise ValueError("CSS selector or button text must be provided")
            await button.click(timeout=TIMEOUT * 1000)
            await self._browser_state.page.wait_for_load_state("networkidle")
            page_source = await self._browser_state.page.content()
            return clean_html(page_source)
        except Exception as e:
            raise ToolException(f"Ошибка при нажатии кнопки: {e}") from e


class ExtractTextArgsSchema(BaseModel):
    css_selector: str = Field(description="CSS селектор элемента.")


class ExtractTextTool(BaseTool):
    name: str = "ExtractText"
    description: str = "Получение текста элемента по CSS селектору элемента."
    args_schema: Optional[ArgsSchema] = ExtractTextArgsSchema

    def __init__(self, browser_state: BrowserState, **kwargs) -> None:
        super().__init__(**kwargs)
        self._browser_state = browser_state

    def _run(self, css_selector: str) -> str:
        raise NotImplementedError

    async def _arun(self, css_selector: str) -> str:
        logger.info("---EXTRACT TEXT---")
        return self._browser_state.page.inner_text(css_selector)


class Element(BaseModel):
    css_selector: str = Field(description="CSS селектор элемента")
    type: str = Field(description="Тип элемента")
    text: Optional[str] = Field(description="Текст элемента")


class SearchElementArgsSchema(BaseModel):
    description: str = Field(description="Описание элемента")


class SearchElementTool(BaseTool):
    name: str = "SearchElement"
    description: str = "Находит элемент по его семантическому описанию"
    args_schema: Optional[ArgsSchema] = SearchElementArgsSchema

    def __init__(self, browser_state: BrowserState, model: BaseChatModel, **kwargs) -> None:
        super().__init__(**kwargs)
        self._browser_state = browser_state
        self._llm_chain = create_structured_output_llm_chain(
            output_schema=Element,
            prompt_template=SEARCH_ELEMENT_PROMPT,
            model=model
        )

    def _run(self, description: str) -> dict[str, str]:
        raise NotImplementedError

    async def _arun(self, description: str) -> dict[str, str]:
        logger.info("---SEARCH ELEMENT---")
        page_source = self._browser_state.page_source
        cleaned_page_source = clean_html(page_source)
        element = await self._llm_chain.ainvoke({
            "description": description, "page_source": cleaned_page_source
        })
        return element.model_dump()
