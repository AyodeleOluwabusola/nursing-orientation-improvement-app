from typing import Optional

from sqlalchemy import Integer
from pyasn1_modules.rfc1902 import Integer
from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum

class Role(str, Enum):
    ADMIN = "ADMIN"
    ORIENTEE = "ORIENTEE"
    PRECEPTOR = "PRECEPTOR"

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str = None
    email: EmailStr
    type: Role
    clinical_background: str
    learning_style: str = None
    personality: str = None
    addition_information: str = None

class UserOut(BaseModel):
    id: int
    first_name: str = None
    last_name: str
    phone_number: str
    email: EmailStr
    type: Role
    clinical_background: str
    learning_style: str
    personality: str
    addition_information: str = None

    model_config = ConfigDict(from_attributes=True)
