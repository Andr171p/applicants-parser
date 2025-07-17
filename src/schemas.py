from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class ListApplicantsSchema(BaseModel):
    aplicants: list[ApplicantsSchema]


class ApplicantsSchema(BaseModel):
    applicant_id: str
    university: str
    direction: str

    model_config = ConfigDict(from_attributes=True)
