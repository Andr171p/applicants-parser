"""CSS селекторы и JS скрипты для парсинга"""

# CSS селектор для получения карточки университета
ORGANIZATION_CARD_SELECTOR = "app-organization-card"
# CSS селектор для получения названия университета
ORGANIZATION_TITLE_SELECTOR = "xpath=//span[@class='title-h3']"
# CSS селектор кнопки для открытия окна фильтрации университетов
FILTER_BUTTON_SELECTOR = "button.filter-button"
# CSS селектор для фильтрации направлений подготовки по форме образования
EDUCATION_FORM_FILTER_SELECTOR = (
    "form[formgroupname='educationForms'] div.text-plain:has-text('{education_form}')"
)
# CSS селектор для фильтрации направлений подготовки по уровню обучения
EDUCATION_LEVEL_FILTER_SELECTOR = (
    "form[formgroupname='educationLevels'] div.text-plain:has-text('{education_level}')"
)
# CSS селектор для получения программы обучения на направление подготовки
EDUCATION_PROGRAM_SELECTOR = "app-education-program-card"
# CSS селектор кнопки для показа ещё некоторого количества направлений подготовки
SEE_MORE_BUTTON_SELECTOR = "button.white.button:has-text('Посмотреть ещё')"
# JS скрипт для извлечения названия профиля обучения
FETCH_PROFILE_SCRIPT = """() => {
        return Array.from(document.querySelectorAll('lib-expansion-panel'))
            .map(el => {
                const root = el.shadowRoot || el;
                const title = root.querySelector('h4.title-h4');
                return title ? title.textContent.trim() : null;
            })
            .filter(Boolean);
    }"""
# CSS селектор для извлечения формы образования
EDUCATION_FORM_SELECTOR = "div.small-text.gray:has-text('Форма обучения') + div.text-plain"
# CSS селектор для получения названия института к которому относится направления подготовки
INSTITUTE_SELECTOR = "div.text-plain.mb-24.ng-star-inserted"
# Полный путь до элемента с количеством бюджетных мест
BUDGET_PLACES_XPATH = (
    "xpath=//li[.//div[contains(@class, 'gray') and text()='Основные места']]"
    "//div[contains(@class, 'bold')]"
)
# CSS селектор для получения количества всех мест на направление подготовки
TOTAL_PLACES_SELECTOR = "div.header-places div.small-text"
# CSS селектор для получения цены образования
EDUCATION_PRICE_SELECTOR = "div.title-h3.mb-8"
# CSS селектор для перехода на страницу с конкурсными списками
LIST_OF_APPLICANTS_SELECTOR = "a:has-text('Списки подавших документы')"
# CSS селектор для открытия таблицы с определёнными цифрами приёма
RECEPTIONS_SELECTOR = "ul.shadow-block"
# CSS селектор кнопки для скачивания рейтинга
DOWNLOAD_AS_TABLE_SELECTOR = "button:has-text('Скачать в виде таблицы')"
