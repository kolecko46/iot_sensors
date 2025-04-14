from sqlalchemy import DECIMAL, DateTime, Index, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import datetime
import decimal

class Base(DeclarativeBase):
    pass


class Books(Base):
    __tablename__ = 'books'
    __table_args__ = (
        Index('id_UNIQUE', 'id', unique=True),
    )

    name: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    id: Mapped[int] = mapped_column(Integer, primary_key=True)


class ClimateData(Base):
    __tablename__ = 'climate_data'

    temperature: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2))
    humidity: Mapped[decimal.Decimal] = mapped_column(DECIMAL(5, 2))
    measure_at: Mapped[datetime.datetime] = mapped_column(DateTime, primary_key=True)


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('id_UNIQUE', 'id', unique=True),
        Index('name_UNIQUE', 'name', unique=True)
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))
