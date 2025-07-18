from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser
    from playwright.sync_api import Browser as SyncBrowser

from langchain_core.tools import BaseTool
from pydantic import model_validator


class BaseBrowserTool(BaseTool):
    """Базовый класс для инструментов автоматизации браузера"""

    sync_browser: SyncBrowser | None = None
    async_browser: AsyncBrowser | None = None

    @model_validator(mode="before")
    def validate_browser_provided(self) -> BaseBrowserTool:
        """Проверка инициализации разных типов браузеров"""
        if self.sync_browser is None and self.async_browser is None:
            raise ValueError("Either browsers instances must be provided!")
        return self

    @classmethod
    def from_browser(
            cls,
            sync_browser: SyncBrowser | None = None,
            async_browser: AsyncBrowser | None = None
    ) -> BaseBrowserTool:
        """Инициализация инструмента через уже готовый браузер."""
        return cls(sync_browser=sync_browser, async_browser=async_browser)

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """Синхронный вызов инструмента."""
        raise NotImplementedError

    async def _arun(self, *args: Any, **kwargs: Any) -> Any:
        """Асинхронный вызов инструмента."""
        raise NotImplementedError
