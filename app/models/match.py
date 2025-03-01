# app/models/match.py
from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.models.base import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    preceptor_id = Column(Integer, ForeignKey("preceptors.id"))
    match_score = Column(Float, default=0.0)
    orientee = relationship("Orientee", backref="matches")
    preceptor = relationship("Preceptor", backref="matches")
