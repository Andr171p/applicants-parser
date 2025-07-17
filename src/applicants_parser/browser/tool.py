from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Any

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser
    from playwright.sync_api import Browser as SyncBrowser

from pydantic import model_validator

from langchain_core.tools import BaseTool


class BaseBrowserTool(BaseTool):
    """Базовый класс для инструментов автоматизации браузера"""

    sync_browser: Optional["SyncBrowser"] = None
    async_browser: Optional["AsyncBrowser"] = None

    @model_validator(mode="before")
    def validate_browser_provided(self) -> BaseBrowserTool:
        """Проверка инициализации разных типов браузеров"""
        if self.sync_browser is None and self.async_browser is None:
            raise ValueError("Either browsers instances must be provided!")
        return self

    @classmethod
    def from_browser(
            cls,
            sync_browser: Optional["SyncBrowser"] = None,
            async_browser: Optional["AsyncBrowser"] = None
    ) -> BaseBrowserTool:
        """Инициализация инструмента через уже готовый браузер"""
        return cls(sync_browser=sync_browser, async_browser=async_browser)

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
