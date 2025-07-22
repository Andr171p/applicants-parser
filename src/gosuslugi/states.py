from typing import TypedDict

from pathlib import Path

from src.core.schemas import Applicant, Direction, University
from src.core.enums import EducationForm
from .constants import EDUCATION_LEVEL


class UniversityState(TypedDict):
    university_url: str
    university: University
    education_forms: list[EducationForm]
    education_levels: list[EDUCATION_LEVEL]
    direction_urls: list[str]


class AdmissionListState(TypedDict):
    direction_url: str
    direction: Direction
    admission_list_files: list[str | Path]
    applicants: list[Applicant]
