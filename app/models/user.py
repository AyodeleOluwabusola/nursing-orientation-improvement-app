from sqlalchemy import Column, Integer, String, Enum
from app.models.base import Base
import enum

class Role(enum.Enum):
    ADMIN = "ADMIN"
    ORIENTEE = "ORIENTEE"
    PRECEPTOR = "PRECEPTOR"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    email = Column(String, unique=True, nullable=False)
    type = Column(Enum(Role), default=Role.ORIENTEE)
    clinical_background = Column(String, nullable=False)
    learning_style = Column(String, nullable=False)
    personality = Column(String, nullable=False)
    # academic_background = Column(String, nullable=True) # for. "Orientee"
    # specialty = Column(String, nullable=True) # for. "Preceptor"
    addition_information = Column(String, nullable=True)
