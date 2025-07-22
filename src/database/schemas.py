from __future__ import annotations

from pydantic import BaseModel, ConfigDict

from .models import ApplicantsModel


class ListApplicantsSchema(BaseModel):
    applicants: list[ApplicantSchema]

    def to_database(self) -> list:
        return [applicant.to_model for applicant in self.applicants]


class ApplicantSchema(BaseModel):
    applicant_id: str
    university: str
    direction: str

    model_config = ConfigDict(from_attributes=True)

    @property
    def to_model(self) -> ApplicantsModel:
        return ApplicantsModel(
            applicant_id=self.applicant_id, university=self.university, direction=self.direction
        )
