from datetime import datetime

from pydantic import BaseModel, ConfigDict

from .enums import Source, EducationForm, Submit


class University(BaseModel):
    """Университет"""
    id: int         # Уникальный ID университета
    name: str       # Название университета
    source: Source  # Источник откуда получен университет
    url: str        # URL университета (источника)

    model_config = ConfigDict(from_attributes=True)


class Direction(BaseModel):
    """Направление подготовки"""
    university_id: int             # ID университета
    name: str                      # Название направления подготовки
    education_form: EducationForm  # Форма обучения
    institute: str                 # Институт
    budget_places: int             # Количество бюджетных мест
    total_places: int              # Всего мест
    education_sale: float          # Цена на обучения

    model_config = ConfigDict(from_attributes=True)


class Applicant(BaseModel):
    """Абитуриент из конкурсного списка"""
    id: int                 # ID абитуриента с Госуслуг
    serial_number: int      # Порядковый номер
    priority: int           # Приоритет
    submit: Submit          # Согласие
    total_points: int       # Сумма баллов
    points: list[int]       # Баллы за ВИ
    additional_points: int  # Дополнительные баллы
    original: bool          # Сдан ли оригинал
    status: str             # Статус заявления
    date: datetime          # Дата подачи заявления

    model_config = ConfigDict(from_attributes=True)
