from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .enums import EducationForm, Source, Submit


class UniversitySchema(BaseModel):
    """Университет"""
    id: int         # Уникальный ID университета
    title: str      # Название университета
    source: Source  # Источник откуда получен университет
    url: str        # URL университета (источника)

    model_config = ConfigDict(from_attributes=True)


class DirectionSchema(BaseModel):
    """Направление подготовки"""
    university_id: int             # ID университета
    code: str                      # Код направления подготовки
    title: str | None              # Название направления подготовки
    education_form: EducationForm  # Форма обучения
    institute: str | None          # Институт
    budget_places: int             # Количество бюджетных мест
    total_places: int              # Всего мест
    education_price: float         # Цена на обучения

    model_config = ConfigDict(from_attributes=True)


class ApplicantSchema(BaseModel):
    """Абитуриент из конкурсного списка"""
    university_id: int               # ID университета
    direction_code: str              # Код направления подготовки
    id: int                          # ID абитуриента с Госуслуг
    place: int                       # Место в конкурсе
    priority: int                    # Приоритет
    submit: Submit                   # Согласие
    total_points: int                # Сумма баллов
    entrance_exam_points: list[int]  # Баллы за ВИ
    additional_points: int           # Баллы за ИД
    without_entrance_exams: bool     # True если с БВИ, False если без
    advantage: str | None = None     # Преимущество

    model_config = ConfigDict(from_attributes=True)
