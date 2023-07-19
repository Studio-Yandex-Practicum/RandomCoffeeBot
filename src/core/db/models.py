from datetime import datetime
from typing import Optional

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import DeclarativeBase, Mapped, backref, mapped_column, relationship


class Base(DeclarativeBase):
    pass
