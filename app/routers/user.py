from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User, Role
from app.schemas.response import APIResponse
from app.schemas.user import UserProfile, UserSignIn, UserCreate, UserProfileReq
from app.services.firebase_auth import verify_firebase_token, verify_password
from app.services.profile_service import create_user_profile, create_user, fetch_orientees_by_preceptor, fetch_preceptor_by_orientee

router = APIRouter()

@router.get("/{user_id}")
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/details/{email}")
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/preceptor/{preceptor_id}")
def retrieve_all_orientees_by_preceptor(preceptor_id: int, db: Session = Depends(get_db)):
    return fetch_orientees_by_preceptor(preceptor_id, db)

@router.get("/orientee/{orientee_id}")
def retrieve_preceptor_for_orientee(orientee_id: int, db: Session = Depends(get_db)):
    return fetch_preceptor_by_orientee(orientee_id, db)


@router.post("")
def create_profile(
        user_data: UserProfileReq,
        db: Session = Depends(get_db),
):
    return  create_user_profile(user_data, db)


# Would not be used by FE
@router.post("/create", status_code=201)
def create_user(
        user_data: UserCreate,
        decoded_token: dict = Depends(verify_firebase_token),
        db: Session = Depends(get_db)
):
    return create_user(user_data, decoded_token, db)


# Would not be used by FE
@router.post("/signin")
def signin_user(
        data: UserSignIn,
        decoded_token: dict = Depends(verify_firebase_token),
        db: Session = Depends(get_db),
):
    # Extract the Firebase UID from the token.
    firebase_uid = decoded_token.get("uid")

    # Look up the user in the SQL database.
    user = db.query(User).filter(User.email == data.email, User.firebase_uid == firebase_uid).first()
    if not user:
        # The user is not found in the database.
        raise HTTPException(
            status_code=404,
            detail="User not found. Please sign up first."
        )

    matches = verify_password(data.password, user.password)
    if not matches:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Return user details if the sign-in is successful.
    return APIResponse(
        status="00",
        message="Sign-in successful",
        data=user
    )
