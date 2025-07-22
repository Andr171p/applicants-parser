__all__ = [
    "ApplicantsModel",
    "DirectionsModel",
    "UniversitysModel",
    "add_all_applicants",
    "add_directions",
    "add_universitys",
]

from .models import ApplicantsModel, DirectionsModel, UniversitysModel
from .session import add_all_applicants, add_directions, add_universitys
