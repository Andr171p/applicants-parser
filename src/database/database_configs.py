import uuid
from datetime import datetime
from typing import Annotated

from sqlalchemy import BIGINT, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column

created_at = Annotated[datetime, mapped_column(server_default=func.now())]
int_pk = Annotated[int, mapped_column(primary_key=True)]
uuid_pk = Annotated[
    uuid.UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
]
int_null = Annotated[int, mapped_column(nullable=False, unique=True)]
big_int_uniq = Annotated[int, mapped_column(BIGINT, nullable=True, unique=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_uniq_null = Annotated[str, mapped_column(unique=True, nullable=True)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
str_nullable = Annotated[str, mapped_column(nullable=False)]
str_def = Annotated[str, mapped_column(default=None)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
