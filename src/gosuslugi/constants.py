from typing import Literal

# Задержка по времени в мс
TIMEOUT = 1000

# Базовый URL адрес Госуслуг.
GOSUSLUGI_URL = "https://www.gosuslugi.ru"
# URL адрес для поиска университетов на Госуслугах.
GOSUSLUGI_SEARCH_URL = "https://www.gosuslugi.ru/vuznavigator/universities?query="
# URL шаблон университета
GOSUSLUGI_UNIVERSITY_URL = "https://www.gosuslugi.ru/vuznavigator/universities/"

# Уровень образования
EDUCATION_LEVEL = Literal["Бакалавриат", "Специалитет", "Базовое высшее"]

# Сообщения об технической ошибке на странице
TECHNICAL_ERROR = "Техническая ошибка"

# Нет баллов за ВИ
NO_POINTS = "Без вступительных испытаний"
ZERO_VALUE = 0

# Поступление по БВИ
WITHOUT_ENTRANCE_EXAMS = "Да"
