from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from app.models.base import Base

class Orientee(Base):
    __tablename__ = "orientees"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    academic_background = Column(String, nullable=True)

    user = relationship("User", backref="orientee_profile")