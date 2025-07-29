from collections.abc import Iterator

from ..constants import UNIVERSITIES_COUNT
from .constants import GOSUSLUGI_UNIVERSITY_URL

START = 1


def extract_direction_code(url: str) -> str:
    """Извлекает код направления подготовки из его URL.

    :param url: URL адрес направления подготовки, например: https://www.gosuslugi.ru/vuznavigator/specialties/2.20.03.01/2/43
    :return Код направления, например: 2.20.03.01
    """
    parts = url.strip("/").split("/")
    index = parts.index("specialties")
    return parts[index + 1]


def extract_university_id(url: str) -> int:
    """Извлекает ID университета из его URL адреса.

    :param url: URL адрес университета на Госуслугах
    :return: ID университета с Госуслуг
    """
    return url.split("/")[-1]  # noqa: PLC0207


def format_row(row: tuple[str]) -> list[str | int]:
    """Приводит уёбищный кортеж к удобному массиву.

    :param row: Уёбищный кортеж
    :return: Пиздатый массив
    """
    return list(map(lambda x: x.replace('"', ""), row[0].split(";")))


def generate_university_urls(start: int = START, end: int = UNIVERSITIES_COUNT) -> Iterator[str]:
    """Генерирует URL университетов на Госуслугах.

    :param start: Начало диапазона включительно
    :param end: Конец диапазона включительно
    :return: Итератор URL университетов.
    """
    for id in range(start, end + 1):
        yield f"{GOSUSLUGI_UNIVERSITY_URL}{id}"


def handle_technical_error() -> ...: ...
