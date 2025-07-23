from __future__ import annotations

from datetime import datetime

from pydantic import field_validator

from ..core.schemas import ApplicantSchema, DirectionSchema
from .constants import NO_POINTS, ZERO_VALUE
from .utils import extract_direction_code


class ApplicantValidator(ApplicantSchema):
    @classmethod
    def from_csv_row(cls, row: list[str | int], **kwargs) -> ApplicantSchema:
        return cls(
            university_id=kwargs.get("university_id"),
            direction_code=kwargs.get("direction_code"),
            id=row[1],
            serial_number=row[0],
            priority=row[2],
            submit=row[3],
            total_points=row[4],
            points=row[5],
            additional_points=row[6],
            status=row[7],
            original=False,  # For test mode
            date=row[8]
        )

    @field_validator("direction_code", mode="before")
    def validate_direction_code(cls, direction_url: str) -> str:
        return extract_direction_code(direction_url)

    @field_validator("points", mode="before")
    def validate_points(cls, points: str) -> list[int]:
        if points == NO_POINTS:
            return [ZERO_VALUE]
        return list(map(int, points.split(" ")))

    @field_validator("date", mode="before")
    def validate_date(cls, date: str) -> datetime:
        return datetime.strptime(date, "%d.%m.%Y в %H:%M")  # noqa: DTZ007


class DirectionValidator(DirectionSchema):
    @field_validator("total_places", mode="before")
    def validate_total_places(cls, total_places: str) -> int:
        return int(
            "".join(
                filter(str.isdigit, total_places
                       .replace(" ", "")
                       .replace("&nbsp;", "")
                       .strip())
            )
        )

    @field_validator("education_price", mode="before")
    def validate_education_price(cls, education_price: str) -> float:
        return float("".join(filter(str.isdigit, education_price.strip())))
