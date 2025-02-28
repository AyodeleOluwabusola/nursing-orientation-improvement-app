# app/models/preceptor.py
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Preceptor(Base):
    __tablename__ = "preceptors"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    specialty = Column(String, nullable=True)

    user = relationship("User", backref="preceptor_profile")
