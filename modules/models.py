from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Books(Base):
    __tablename__ = 'books'
    __table_args__ = (
        Index('id_UNIQUE', 'id', unique=True),
    )

    name: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('id_UNIQUE', 'id', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))

class ClimateData(Base):
    __tablename__ = 'climate_data'

    temperature: Mapped[str] = mapped_column(Integer)
    humidity: Mapped[str] = mapped_column(Integer)
    measured_at: Mapped[str] = mapped_column(String(45), primary_key=True)
