from datetime import date
from enum import StrEnum
from typing import Optional

from sqlalchemy import ForeignKey, Integer, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

SERVER_DEFAULT_TIME = func.current_timestamp()


class StatusEnum(StrEnum):
    IN_MEETING = "IN_MEETING"
    WAITING_MEETING = "WAITING_MEETING"
    NOT_INVOLVED = "NOT_INVOLVED"


class MatchStatusEnum(StrEnum):
    ONGOING = "ONGOING"
    CLOSED = "CLOSED"


class MatchReviewAnswerEnum(StrEnum):
    IS_COMPLETE = "IS_COMPLETE"
    IS_NOT_COMPLETE = "IS_NOT_COMPLETE"


class Base(DeclarativeBase):
    """Base class for models"""

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[date] = mapped_column(server_default=SERVER_DEFAULT_TIME, nullable=False)
    updated_at: Mapped[date] = mapped_column(
        nullable=False, onupdate=SERVER_DEFAULT_TIME, server_default=SERVER_DEFAULT_TIME
    )


class Admin(Base):
    __tablename__ = "admin"

    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    user_id: Mapped[int] = mapped_column(String(200), unique=True, nullable=False)


class User(Base):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[StatusEnum] = mapped_column(default=StatusEnum.NOT_INVOLVED, nullable=False)

    matches: Mapped[list["UsersMatch"]] = relationship(
        primaryjoin="or_(User.id==UsersMatch.matched_user_one, User.id==UsersMatch.matched_user_two)"
    )


class UsersMatch(Base):
    __tablename__ = "usersmatch"

    matched_user_one: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    matched_user_two: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    status: Mapped[MatchStatusEnum] = mapped_column(default=MatchStatusEnum.ONGOING, nullable=False)

    object_user_one = relationship("User", foreign_keys=[matched_user_one], backref="matches_as_user_one")
    object_user_two = relationship("User", foreign_keys=[matched_user_two], backref="matches_as_user_two")
    match_review: Mapped["MatchReview"] = relationship("MatchReview", backref="usersmatch")


class MatchReview(Base):
    __tablename__ = "match_review"

    usersmatch_id: Mapped[int] = mapped_column(Integer(), ForeignKey("usersmatch.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user_answer: Mapped[Optional[MatchReviewAnswerEnum]] = mapped_column(nullable=True)
