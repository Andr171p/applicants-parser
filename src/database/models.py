from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import Mapped

from .database_configs import (
    Base,
    bool_null,
    float_null,
    int_null,
    int_pk,
    list_int,
    str_null,
    str_null_true,
)


class UniversitiesModel(Base):
    """Университет"""

    __tablename__ = "universitys"

    id: Mapped[int_pk]  # Уникальный ID университета
    title: Mapped[str_null]  # Название университета
    source: Mapped[str_null]  # Источник откуда получен университет
    url: Mapped[str_null]  # URL университета (источника)


class DirectionsModel(Base):
    """Направление подготовки"""

    __tablename__ = "directions"

    university_id: Mapped[int_null]  # ID университета
    code: Mapped[str_null]  # Код направления подготовки
    title: Mapped[str_null]  # Название направления подготовки
    education_form: Mapped[str_null]  # Форма обучения
    institute: Mapped[str_null_true]  # Институт
    budget_places: Mapped[int_null]  # Количество бюджетных мест
    total_places: Mapped[int_null]  # Всего мест
    education_price: Mapped[float_null]  # Цена на обучения

    __table_args__ = (PrimaryKeyConstraint("university_id", "code", name="direction_pk"),)


class ApplicantsModel(Base):
    """Абитуриент из конкурсного списка"""

    __tablename__ = "applicants"

    university_id: Mapped[int_null]  # ID университета
    direction_code: Mapped[str_null]  # Код направления подготовки
    id: Mapped[int_null]  # ID абитуриента с Госуслуг
    place: Mapped[int_null]  # Порядковый номер
    priority: Mapped[int_null]  # Приоритет
    submit: Mapped[str_null]  # Согласие
    total_points: Mapped[int_null]  # Сумма баллов
    entrance_exam_points: Mapped[list_int]  # Баллы за ВИ
    additional_points: Mapped[int_null]  # Дополнительные баллы
    without_entrance_exams: Mapped[bool_null]  # Сдан ли оригинал
    advantage: Mapped[str_null_true]  # Статус заявления

    __table_args__ = (PrimaryKeyConstraint("university_id", "id", name="applicant_pk"),)
