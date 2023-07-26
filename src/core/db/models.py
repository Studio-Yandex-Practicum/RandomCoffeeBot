from datetime import date

from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

SERVER_DEFAULT_TIME = func.current_timestamp()


class Base(DeclarativeBase):
    "Base class for models"

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(server_default=SERVER_DEFAULT_TIME, nullable=False)
    updated_at: Mapped[date] = mapped_column(
        nullable=False, onupdate=SERVER_DEFAULT_TIME, server_default=SERVER_DEFAULT_TIME
    )
    __name__: Mapped[str]
