from sqlalchemy import Column, Integer, ForeignKey, Float
from app.models.base import Base

class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    orientee_id = Column(Integer, ForeignKey("users.id"))
    preceptor_id = Column(Integer, ForeignKey("users.id"))
