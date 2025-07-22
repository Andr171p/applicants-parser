from enum import StrEnum


class Source(StrEnum):
    """Источник университета"""
    GOSUSLUGI = "GOSUSLUGI"
    SITE = ""


class EducationForm(StrEnum):
    """Формы обучения"""
    FULL_TIME = "Очная"
    PART_TIME = "Очно-заочное"
    EXTRAMURAL = "Заочное"


class Submit(StrEnum):
    """Согласие на зачисление"""
    PAPER = "Бумажное"
    ELECTRONIC = "Электронное"
    NOT_SUBMITTED = "_"


class Status(StrEnum):
    """Статусы заявления"""
    CANCELED = "Конкурсная группа исключена"
    AWAITED_RESULTS = "Ожидаются результаты испытаний"
    IN_COMPETITION = "Участвуете в конкурсе"
