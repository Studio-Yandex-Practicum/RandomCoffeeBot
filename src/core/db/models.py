from datetime import date
from enum import StrEnum

from sqlalchemy import String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

SERVER_DEFAULT_TIME = func.current_timestamp()


class StatusEnum(StrEnum):
    IN_MEETING = "IN_MEETING"
    WAITING_MEETING = "WAITING_MEETING"
    NOT_INVOLVED = "NOT_INVOLVED"


class Base(DeclarativeBase):
    "Base class for models"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(server_default=SERVER_DEFAULT_TIME, nullable=False)
    updated_at: Mapped[date] = mapped_column(
        nullable=False, onupdate=SERVER_DEFAULT_TIME, server_default=SERVER_DEFAULT_TIME
    )
    __name__: Mapped[str]


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(nullable=False)
