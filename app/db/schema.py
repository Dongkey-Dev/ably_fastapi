from email.policy import default
from enum import unique
from sqlalchemy import Column, ForeignKey, INT, BINARY, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from app.db.mixin import BaseMixin
import uuid

Base = declarative_base()

class Users(Base, BaseMixin):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key = True, default=uuid.uuid4)
    email = Column(String(length=255), nullable=False, unique=True)
    nickname = Column(String(length=255), nullable=False)
    username = Column(String(length=255), nullable=False)
    phone = Column(String(length=255), nullable=False, unique=True)
    pswd = Column(String(length=255), nullable=False)