from typing import Optional

from sqlalchemy import Integer
from pyasn1_modules.rfc1902 import Integer
from pydantic import BaseModel, EmailStr
from enum import Enum

class Role(str, Enum):
    ADMIN = "ADMIN"
    ORIENTEE = "ORIENTEE"
    PRECEPTOR = "PRECEPTOR"

class UserCreate(BaseModel):
    academic_background: str = None
    email: EmailStr
    type: Role
    specialty: Optional[str] = None  # e.g. "Cardiology"
    clinical_background: str
    learning_style: str = None
    personality: str = None

class UserOut(BaseModel):
    id: str
    email: EmailStr
    specialty: Optional[str] = None

    class Config:
        orm_mode = True
