from pydantic import field_validator

from ...core.schemas import Direction


class DirectionValidator(Direction):
    @field_validator("total_places")
    def validate_total_places(cls, total_places: str) -> int:
        return int("".join(filter(str.isdigit, total_places.strip())))

    @field_validator("education_price")
    def validate_education_price(cls, education_price: str) -> float:
        return float("".join(filter(str.isdigit, education_price.strip())))
