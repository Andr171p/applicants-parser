from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from ..database import ApplicantsModel, DirectionsModel, UniversitysModel
from .enums import EducationForm, Source, Submit


class UniversitySchema(BaseModel):
    """Университет"""

    university_id: int  # Уникальный ID университета
    title: str  # Название университета
    source: Source  # Источник откуда получен университет
    url: str  # URL университета (источника)

    model_config = ConfigDict(from_attributes=True)

    @property
    def to_model(self) -> UniversitysModel:
        return UniversitysModel(
            university_id=self.university_id,
            title=self.title,
            source=self.source,
            url=self.url,
        )


class DirectionSchema(BaseModel):
    """Направление подготовки"""

    university_id: int  # ID университета
    code: str  # Код направления подготовки
    title: str  # Название направления подготовки
    education_form: EducationForm  # Форма обучения
    institute: str | None  # Институт
    budget_places: int  # Количество бюджетных мест
    total_places: int  # Всего мест
    education_price: float  # Цена на обучения

    model_config = ConfigDict(from_attributes=True)

    @property
    def to_model(self) -> DirectionsModel:
        return DirectionsModel(
            university_id=self.university_id,
            code=self.code,
            title=self.title,
            education_form=self.education_form,
            institute=self.institute,
            budget_places=self.budget_places,
            total_places=self.total_places,
            education_price=self.education_price,
        )


class ListApplicantsSchema(BaseModel):
    applicants: list[ApplicantSchema]

    def to_database(self) -> list:
        return [applicant.to_model for applicant in self.applicants]


class ApplicantSchema(BaseModel):
    """Абитуриент из конкурсного списка"""

    university_id: int  # ID университета
    direction_code: str  # Код направления подготовки
    applicant_id: int  # ID абитуриента с Госуслуг
    serial_number: int  # Порядковый номер
    priority: int  # Приоритет
    submit: Submit  # Согласие
    total_points: int  # Сумма баллов
    points: list[int]  # Баллы за ВИ
    additional_points: int  # Дополнительные баллы
    original: bool  # Сдан ли оригинал
    status: str  # Статус заявления
    date: datetime  # Дата подачи заявления

    model_config = ConfigDict(from_attributes=True)

    @property
    def to_model(self) -> ApplicantsModel:
        return ApplicantsModel(
            university_id=self.university_id,
            direction_code=self.direction_code,
            applicant_id=self.applicant_id,
            serial_number=self.serial_number,
            priority=self.priority,
            submit=self.submit,
            total_points=self.total_points,
            points=self.points,
            additional_points=self.additional_points,
            original=self.original,
            status=self.status,
            date=self.date,
        )
