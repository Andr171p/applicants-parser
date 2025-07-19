from __future__ import annotations

from typing import TYPE_CHECKING

from collections.abc import Sequence

if TYPE_CHECKING:
    from playwright.async_api import Browser as AsyncBrowser
    from playwright.async_api import Page as AsyncPage
    from playwright.sync_api import Browser as SyncBrowser
    from playwright.sync_api import Page as SyncPage

from ..utils import run_async

ATTRIBUTE = "innerText"
TIMEOUT = 2000  # Время в мс


async def aget_current_page(browser: AsyncBrowser) -> AsyncPage:
    """
    Асинхронно получает текущую страницу браузера.

    :param browser:
    :return: Текущая страница браузера.
    """
    if not browser.contexts:
        context = await browser.new_context()
        return await context.new_page()
    context = browser.contexts[0]
    if not context.pages:
        return await context.new_page()
    return context.pages[-1]


def get_current_page(browser: SyncBrowser) -> SyncPage:
    """
    Получает текущую страницу браузера.

    :param browser: Синхронный Playwright браузер.
    :return Текущая страница браузера.
    """
    if not browser.contexts:
        context = browser.new_context()
        return context.new_page()
    context = browser.contexts[0]
    if not context.pages:
        return context.new_page()
    return context.pages[-1]


def create_async_playwright_browser(
    headless: bool = False, args: list[str] | None = None
) -> AsyncBrowser:
    """
    Фабрика для создания асинхронного Playwright браузера.

    :param headless: Запускать ли браузер в headless режиме, по умолчанию False.
    :param args: Аргументы дял передачи в браузер chromium.
    :return: AsyncBrowser асинхронный Playwright браузер.
    """
    from playwright.async_api import async_playwright  # noqa: PLC0415

    browser = run_async(async_playwright().start())
    return run_async(browser.chromium.launch(headless=headless, args=args))


def create_sync_playwright_browser(
    headless: bool = False, args: list[str] | None = None
) -> SyncBrowser:
    """
    Фабрика для создания синхронного Playwright браузера.

    :param headless: Запускать ли браузер в headless режиме, по умолчанию False.
    :param args: Аргументы дял передачи в браузер chromium.
    :return: SyncBrowser синхронный Playwright браузер.
    """
    from playwright.sync_api import sync_playwright  # noqa: PLC0415

    browser = sync_playwright().start()
    return browser.chromium.launch(headless=headless, args=args)


async def aget_elements(
    page: AsyncPage, css_selector: str, attributes: Sequence[str]
) -> list[dict[str, str]]:
    """
    Асинхронно получает элементы на странице по заданному CSS селектору.

    :param page: Текущая страница.
    :param css_selector: CSS селектор для поиска.
    :param attributes: Набора атрибутов, которые нужно получить.
    :return: Список найденных элементов.
    """
    elements = await page.query_selector_all(css_selector)
    results: list[dict[str, str]] = []
    for element in elements:
        result: dict[str, str] = {}
        for attribute in attributes:
            if attribute == ATTRIBUTE:
                value = await element.inner_text()
            else:
                value = await element.get_attribute(attribute)
            if value is not None and value.strip() != "":
                result[attribute] = value
        if result:
            results.append(result)
    return results


def get_elements(
    page: SyncPage, css_selector: str, attributes: Sequence[str]
) -> list[dict[str, str]]:
    """
    Синхронно получает элементы на странице по заданному CSS селектору.

    :param page: Текущая страница.
    :param css_selector: CSS селектор для поиска.
    :param attributes: Набора атрибутов, которые нужно получить.
    :return: Список найденных элементов.
    """
    elements = page.query_selector_all(css_selector)
    results: list[dict[str, str]] = []
    for element in elements:
        result: dict[str, str] = {}
        for attribute in attributes:
            if attribute == ATTRIBUTE:
                value = element.inner_text()
            else:
                value = element.get_attribute(attribute)
            if value is not None and value.strip() != "":  # noqa: PLC1901
                result[attribute] = value
        if result:
            results.append(result)
    return results


async def ascroll_to_click(page: AsyncPage, css_selector: str) -> bool:
    """Асинхроно скролит страницу до нужного элемента и нажимает его.

    :param page: Асинхронный экземпляр страницы.
    :param css_selector: CSS селектор элемента, который нужно найти.
    :return True если элемент нажат успешно, False если нет.
    """
    element = await page.query_selector(css_selector)
    if not element:
        return False
    await element.scroll_into_view_if_needed()
    await element.click()
    return True
