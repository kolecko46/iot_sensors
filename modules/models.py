from sqlalchemy import Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        Index('id_UNIQUE', 'id', unique=True),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    password: Mapped[str] = mapped_column(String(255))

class ClimateData(Base):
    __tablename__ = 'dht11_data'

    temperature: Mapped[str] = mapped_column(Integer)
    humidity: Mapped[str] = mapped_column(Integer)
    measured_at: Mapped[str] = mapped_column(String(45), primary_key=True)