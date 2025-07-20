from typing import Literal

# Задержка по врнмени в мс
TIMEOUT = 1000

# Базовый URL адрес Госуслуг.
GOSUSLUGI_URL = "https://www.gosuslugi.ru"
# URL адрес для поиска университетов на Госуслугах.
GOSUSLUGI_SEARCH_URL = "https://www.gosuslugi.ru/vuznavigator/universities?query="

# Уровень образования
EDUCATION_LEVEL = Literal["Бакалавриат", "Специалитет", "Базовое высшее"]

# Сообщения об ошибка на странице
TECHNICAL_ERROR = "Техническая ошибка"

# CSS селекторы и JS скрипты для парсинга
ORGANIZATION_SELECTOR = "app-organization-card"
FILTER_BUTTON_SELECTOR = "button.filter-button"
EDUCATION_FORM_FILTER_SELECTOR = (
    "form[formgroupname='educationForms'] div.text-plain:has-text('{education_form}')"
)
EDUCATION_LEVEL_FILTER_SELECTOR = (
    "form[formgroupname='educationLevels'] div.text-plain:has-text('{education_level}')"
)
EDUCATION_PROGRAM_SELECTOR = "app-education-program-card"
SEE_MORE_BUTTON_SELECTOR = "button.white.button:has-text('Посмотреть ещё')"
FETCH_PROFILE_SCRIPT = """() => {
        return Array.from(document.querySelectorAll('lib-expansion-panel'))
            .map(el => {
                const root = el.shadowRoot || el;
                const title = root.querySelector('h4.title-h4');
                return title ? title.textContent.trim() : null;
            })
            .filter(Boolean);
    }"""
EDUCATION_FORM_SELECTOR = "div.small-text.gray:has-text('Форма обучения') + div.text-plain"
INSTITUTE_SELECTOR = "div.text-plain.mb-24.ng-star-inserted"
BUDGET_PLACES_XPATH = (
    "xpath=//li[.//div[contains(@class, 'gray') and text()='Основные места']]"
    "//div[contains(@class, 'bold')]"
)
TOTAL_PLACES_SELECTOR = "div.header-places div.small-text"
EDUCATION_PRICE_SELECTOR = "div.title-h3.mb-8"
