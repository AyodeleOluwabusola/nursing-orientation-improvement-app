# app/routers/user.py
from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4

from sqlalchemy.orm import Session

from app.database import get_db
# Import db from firebase_app (the Firestore client)
from app.firebase_app import db
from pydantic import BaseModel
from app.models.user import User, Role
from app.schemas.user import UserOut, UserCreate
from app.services.profile_service import create_user_profile

router = APIRouter()

@router.get("/{user_id}", response_model=UserCreate)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.post("", response_model=UserCreate)
def create_user(
        user_data: UserCreate,
        db: Session = Depends(get_db)
        # current_user: dict = Depends(verify_firebase_token)
):
    return  create_user_profile(user_data, db)