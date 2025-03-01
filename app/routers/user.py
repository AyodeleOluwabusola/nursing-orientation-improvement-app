from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, Role
from app.schemas.user import UserCreate
from app.services.profile_service import create_user_profile, fetch_orientees_by_preceptor

router = APIRouter()

@router.get("/{user_id}", response_model=UserCreate)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/preceptor/{preceptor_id}")
def retrieve_all_orientees_by_preceptor(preceptor_id: int, db: Session = Depends(get_db)):
    return fetch_orientees_by_preceptor(preceptor_id, db)

@router.post("", response_model=UserCreate)
def create_profile(
        user_data: UserCreate,
        db: Session = Depends(get_db)
        # current_user: dict = Depends(verify_firebase_token)
):
    return  create_user_profile(user_data, db)