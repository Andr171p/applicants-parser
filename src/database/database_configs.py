from typing import Annotated

import uuid
from datetime import datetime

from sqlalchemy import ARRAY, BIGINT, Integer, Text, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, mapped_column

created_at = Annotated[datetime, mapped_column(server_default=func.now())]
int_pk = Annotated[int, mapped_column(primary_key=True)]
uuid_pk = Annotated[
    uuid.UUID, mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
]
list_int = Annotated[list[int], mapped_column(ARRAY(Integer), nullable=False)]
bool_null = Annotated[bool, mapped_column(nullable=False)]
int_null = Annotated[int, mapped_column(nullable=False)]
float_null = Annotated[float, mapped_column(nullable=False)]
big_int_uniq = Annotated[int, mapped_column(BIGINT, nullable=True, unique=True)]
text_null_true = Annotated[str, mapped_column(Text, nullable=True)]
str_uniq = Annotated[str, mapped_column(unique=True, nullable=False)]
str_uniq_null = Annotated[str, mapped_column(unique=True, nullable=True)]
str_null_true = Annotated[str, mapped_column(nullable=True)]
str_null = Annotated[str, mapped_column(nullable=False)]
str_def = Annotated[str, mapped_column(default=None)]


class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True
