from datetime import date

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.sql import func


class Base(DeclarativeBase):
    """Base class for models"""

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(
        server_default=func.current_timestamp()
    )
    updated_at: Mapped[date] = mapped_column(
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp()
    )
