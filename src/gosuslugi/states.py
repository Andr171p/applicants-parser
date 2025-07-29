from typing import Literal, TypedDict

from pathlib import Path

from ..core import ApplicantSchema, DirectionSchema, UniversitySchema
from ..core.enums import EducationForm
from .constants import EDUCATION_LEVEL


class UniversityState(TypedDict):
    """Состояние графа для парсинга конкурсных списков.

    :param university_url: URL текущего университета, инициализируется при вызове графа.
    :param university: Текущий университет.
    :param education_forms: Формы обучения для фильтрации направлений подготовки,
    задаются при вызове графа.
    :param direction_urls: URL адреса всех направлений подготовки университета
    удовлетворяющих фильтрам.
    :param message: Сообщение о выполнении работы графа.
    """

    university_url: str
    university: UniversitySchema
    education_forms: list[EducationForm]
    education_levels: list[EDUCATION_LEVEL]
    direction_urls: list[str]
    message: Literal["FINISH", "ERROR"]


class AdmissionListState(TypedDict):
    """Состояние графа для парсинга конкурсных списков
    на конкретное направление подготовки.

    :param university_id: ID университета с Госуслуг.
    :param direction_url: URL адрес направления подготовки.
    :param direction: Полученное направление подготовки.
    :param receptions2admission_list_files: Скаченные файлы с конкурсными списками.
    :param applicants: Полученные абитуриенты.
    """

    university_id: int
    direction_url: str
    direction: DirectionSchema
    # admission_list_files: list[str | Path]
    receptions2admission_list_files: dict[str, str | Path]
    applicants: list[ApplicantSchema]
