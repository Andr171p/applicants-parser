from datetime import datetime

from pydantic import ConfigDict
from sqlalchemy.orm import Mapped

from ..core import EducationForm, Source, Submit
from .database_configs import Base, bool_null, float_null, int_null, str_null


class UniversitysModel(Base):
    """Университет"""

    __tablename__ = "universitys"

    university_id: Mapped[int_null]  # Уникальный ID университета
    title: Mapped[str_null]  # Название университета
    source: Mapped[Source]  # Источник откуда получен университет
    url: Mapped[str_null]  # URL университета (источника)

    model_config = ConfigDict(from_attributes=True)


class DirectionsModel(Base):
    """Направление подготовки"""

    __tablename__ = "directions"

    university_id: Mapped[int_null]  # ID университета
    code: Mapped[str_null]  # Код направления подготовки
    title: Mapped[str_null]  # Название направления подготовки
    education_form: Mapped[EducationForm]  # Форма обучения
    institute: Mapped[str_null] | None  # Институт
    budget_places: Mapped[int_null]  # Количество бюджетных мест
    total_places: Mapped[int_null]  # Всего мест
    education_price: Mapped[float_null]  # Цена на обучения

    model_config = ConfigDict(from_attributes=True)


class ApplicantsModel(Base):
    """Абитуриент из конкурсного списка"""

    __tablename__ = "applicants"

    university_id: Mapped[int_null]  # ID университета
    direction_code: Mapped[str_null]  # Код направления подготовки
    applicant_id: Mapped[int_null]  # ID абитуриента с Госуслуг
    serial_number: Mapped[int_null]  # Порядковый номер
    priority: Mapped[int_null]  # Приоритет
    submit: Mapped[Submit]  # Согласие
    total_points: Mapped[int_null]  # Сумма баллов
    points: list[Mapped[int_null]]  # Баллы за ВИ
    additional_points: Mapped[int_null]  # Дополнительные баллы
    original: Mapped[bool_null]  # Сдан ли оригинал
    status: Mapped[str_null]  # Статус заявления
    date: datetime  # Дата подачи заявления

    model_config = ConfigDict(from_attributes=True)
