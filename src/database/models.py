from sqlalchemy.orm import Mapped

from .database_configs import Base, created_at, int_pk, str_null_true


class ApplicantsModel(Base):
    __tablename__ = "applicants"

    id: Mapped[int_pk]
    applicant_id: Mapped[str_null_true]
    university: Mapped[str_null_true]
    direction: Mapped[str_null_true]
    created_at: Mapped[created_at]
