from pydantic import field_validator

from ..core import DirectionSchema


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
