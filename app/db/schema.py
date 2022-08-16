from uuid import uuid4

import sqlalchemy
from app.db.mixin import BaseMixin
from sqlalchemy import Column, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base

metadata = sqlalchemy.MetaData()

UsersTable = sqlalchemy.Table(
    "users",
    metadata,
    sqlalchemy.Column("id", UUID(as_uuid=True),
                      primary_key=True, default=uuid4()),
    sqlalchemy.Column("email", sqlalchemy.String),
    sqlalchemy.Column("nickname", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("phone", sqlalchemy.String),
    sqlalchemy.Column("pswd", sqlalchemy.String),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, default=func.now()),
    sqlalchemy.Column("updated_at", sqlalchemy.DateTime,
                      default=func.now(), onupdate=func.now())
)


Base = declarative_base()


class Users(Base, BaseMixin):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    email = Column(String(length=255), nullable=False, unique=True)
    nickname = Column(String(length=255), nullable=False)
    username = Column(String(length=255), nullable=False)
    phone = Column(String(length=255), nullable=False, unique=True)
    pswd = Column(String(length=255), nullable=False)
