from __future__ import annotations

from pydantic import field_validator

from ..core.schemas import ApplicantSchema, DirectionSchema
from .constants import NO_POINTS, WITHOUT_ENTRANCE_EXAMS, ZERO_VALUE
from .utils import extract_direction_code


class ApplicantValidator(ApplicantSchema):
    @classmethod
    def from_csv_row(cls, row: dict[str, str | int], **kwargs) -> ApplicantSchema:
        return cls(
            university_id=kwargs.get("university_id"),
            direction_code=kwargs.get("direction_code"),
            reception=kwargs.get("reception"),
            id=row["ID участника"],
            place=row["Место в конкурсе"],
            priority=row["Приоритет конкурса"],
            submit=row["Подано согласие"],
            total_points=row["Сумма баллов"],
            entrance_exam_points=row["Баллы за ВИ"],
            additional_points=row["Баллы за ИД"],
            without_entrance_exams=row["БВИ"],
            advantage=row["Преимущественное право"],
        )

    @field_validator("direction_code", mode="before")
    def validate_direction_code(cls, direction_url: str) -> str:
        return extract_direction_code(direction_url)

    @field_validator("total_points", mode="before")
    def validate_total_points(cls, total_points: str | int) -> int:
        if isinstance(total_points, str) and total_points == "—":
            return ZERO_VALUE
        return int(total_points)

    @field_validator("entrance_exam_points", mode="before")
    def validate_entrance_exam_points(cls, entrance_exam_points: str | int) -> list[int]:
        if entrance_exam_points == NO_POINTS:
            return [ZERO_VALUE]
        if isinstance(entrance_exam_points, int):
            return [entrance_exam_points]
        return list(map(int, entrance_exam_points.split(" ")))

    @field_validator("without_entrance_exams", mode="before")
    def validate_without_entrance_exams(cls, without_entrance_exams: str) -> bool:
        return without_entrance_exams == WITHOUT_ENTRANCE_EXAMS

    @field_validator("advantage", mode="before")
    def validate_advantage(cls, advantage: str) -> str | None:
        if advantage == "—":
            return None
        return advantage


class DirectionValidator(DirectionSchema):
    @field_validator("total_places", mode="before")
    def validate_total_places(cls, total_places: str) -> int:
        return int(
            "".join(
                filter(str.isdigit, total_places.replace(" ", "").replace("&nbsp;", "").strip())
            )
        )

    @field_validator("education_price", mode="before")
    def validate_education_price(cls, education_price: str) -> float:
        return float("".join(filter(str.isdigit, education_price.strip())))
