from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.match import Match
from app.models.user import User
from app.schemas.response import APIResponse
from app.schemas.user import UserProfile, UserOut, UserCreate
from app.services.firebase_auth import hash_password
from app.services.match_service import get_background

import requests
import json

def create_user_profile(user_data: UserProfile, token: dict, db: Session):

    new_user = User(
        email=user_data.email,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone_number=user_data.phone_number,
        type=user_data.type,
        clinical_background=user_data.clinical_background,
        learning_style=user_data.learning_style,
        personality=user_data.personality,
        addition_information=user_data.addition_information
    )
    db.add(new_user)
    db.commit()
    db.flush()

    print("ID Value: ", new_user.id)
    if (user_data.type == "PRECEPTOR"):
        # Call Vector database
        response = embed_preceptor(new_user.id, db)
        if response.get("error"):
            raise HTTPException(status_code=400, detail="Failed to register preceptor")


    return APIResponse(
            status="00",
            message="User profile created successfully",
            data=new_user
        )



def retrieve_from_token(decoded_token: dict, db: Session):
    # Require that the user's email is verified.
    if not decoded_token.get("email_verified", False):
        raise HTTPException(
            status_code=401,
            detail="Email not verified. Please verify your email before signing up."
        )

    firebase_uid = decoded_token.get("uid")
    email = decoded_token.get("email")

    # Ensure the token provides the necessary details.
    if not firebase_uid or not email:
        raise HTTPException(
            status_code=400,
            detail="Firebase token must include both uid and email."
        )

    # Check if the user already exists in the SQL database.
    user = db.query(User).filter(User.firebase_uid == firebase_uid).first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="User already exists in the database."
        )

    return firebase_uid, email

def create_user(user_data: UserCreate, token, db: Session):

    firebase_uid, email  = retrieve_from_token(token, db)
    hash_password(user_data.password)
    new_user = User(
        firebase_uid=firebase_uid,
        email=email,
        password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.flush()

    print("ID Value: ", new_user.id)
    return APIResponse(
        status="00",
        message="User created successfully",
        data=new_user.email
    )


def fetch_orientees_by_preceptor(preceptor_id: int, db: Session):
    # Retrieve all matches where preceptor_id equals the provided value
    matches = db.query(Match).filter(Match.preceptor_id == preceptor_id).all()
    if not matches:
        raise HTTPException(status_code=404, detail="No matches found for this preceptor")

    # Extract orientee IDs from the matches
    orientee_ids = [match.orientee_id for match in matches]
    print("orientee_ids: ", orientee_ids)

    orientees = []
    for user_id in orientee_ids:
        orientee = db.query(User).filter(User.id == user_id).first()
        if orientee:
            orientees.append(orientee)

    data = [UserOut.from_orm(orientee) for orientee in orientees]
    print("orientees data: ", data)

    return APIResponse(
        status="00",
        message="All Orientees matched to preceptor successfully retrieved",
        data=data
    )

def embed_preceptor(preceptor_id: int, db: Session):

    information = get_background(preceptor_id, db)

    payload = {"user_id": preceptor_id, "information": information}

    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(settings.ADD_MENTOR, data=json.dumps(payload), headers=headers)

    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", json.dumps(response.json(), indent=4))
    except Exception:
        print("Response Text:", response.text)

    if response.status_code != 200:
        return {"error": "Failed Register Preceptor"}

    return {"status": "00", "message": "Added mentor successfully"}

