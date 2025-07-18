from datetime import datetime

from pydantic import BaseModel


class University(BaseModel):
    id: int
    name: str


class Direction(BaseModel):
    university_id: int
    name: str
    places: int
    total: int
    is_yes: int


class Applicant(BaseModel):
    id: int
    applicant_id: int
    priority: int
    original: bool
    points: int
    score: list[int]
    additional_points: int
    status: str
    date: datetime
