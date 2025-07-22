from typing import TypedDict

from pathlib import Path

from src.core.enums import EducationForm

from ..core import ApplicantSchema, DirectionSchema, UniversitySchema
from .constants import EDUCATION_LEVEL


class UniversityState(TypedDict):
    university_url: str
    university: UniversitySchema
    education_forms: list[EducationForm]
    education_levels: list[EDUCATION_LEVEL]
    direction_urls: list[str]


class AdmissionListState(TypedDict):
    direction_url: str
    direction: DirectionSchema
    admission_list_files: list[str | Path]
    applicants: list[ApplicantSchema]
