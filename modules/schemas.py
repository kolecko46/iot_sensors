from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class BookBody(BaseModel):
    name: str
    author: str

class GetBook(BaseModel):
    name: str

class User(BaseModel):
    name: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: str

class Dht11Data(BaseModel):
    temperature: int
    humidity: int
    measured_at: datetime