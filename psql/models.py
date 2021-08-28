"""
Description models for create forms database
"""
from datetime import datetime, timezone

from sqlalchemy import (
    Column, Integer, String, Boolean,
    ForeignKey, DateTime, Enum, JSON, Index, UniqueConstraint
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime as DateTimeType
from sqlalchemy.types import TypeDecorator


Base = declarative_base()


# class utcnow(expression.FunctionElement):
#     type = DateTimeType()


# @compiles(utcnow, 'postgresql')
# def pg_utcnow(element, compiler, **kw):
#     return "TIMEZONE('utc', CURRENT_TIMESTAMP)"
#
#
# class TimeStamp(TypeDecorator):
#     impl = DateTime
#     LOCAL_TIMEZONE = datetime.utcnow().astimezone().tzinfo
#
#     def process_bind_param(self, value: datetime, dialect):
#         if value is None:
#             return None
#
#         if value.tzinfo is None:
#             value = value.astimezone(self.LOCAL_TIMEZONE)
#
#         return value.astimezone(timezone.utc)
#
#     def process_result_value(self, value, dialect):
#         if value is None:
#             return None
#
#         if value.tzinfo is None:
#             return value.replace(tzinfo=timezone.utc)
#
#         return value.astimezone(timezone.utc)


class Form(Base):
    __tablename__ = 'form'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    origin_doc_link = Column(String, nullable=True)
    description = Column(String, nullable=True)
    fields_config = Column(JSON, nullable=True)
    # created_at = Column(DateTimeType, server_default=datetime.utcnow())

    # __table_args__ = (
    #     Index("forms_last_name_idx", "last_name"),
    #     UniqueConstraint("name", "dealer_code", name="form_name_uc"),
    # )

    def __repr__(self):
        return "<Form ('%s')>" % self.last_name