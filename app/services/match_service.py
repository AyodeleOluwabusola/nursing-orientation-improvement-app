from fastapi import Depends
from sqlalchemy.orm import Session
from app.core.config import settings
from app.database import get_db
from app.models.match import Match
from app.models.user import User
import requests
import json

from app.schemas.match import MatchRetrieve
from app.schemas.response import APIResponse
from app.schemas.user import UserOut


def retrieve_all_possible_matches(orientee_id: int, db: Session):
    orientee = db.query(User).filter(User.id == orientee_id).first()

    if not orientee:
        return {"error": "Orientee not found"}


    background = get_background(orientee_id, db)
    payload = {"background": background}
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(settings.MATCH_URL, data=json.dumps(payload), headers=headers)
    if response.status_code != 200:
        return {"error": "Failed to match orientee"}

    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", json.dumps(response.json(), indent=4))
    except Exception:
        print("Response Text:", response.text)

    # Convert response to JSON
    data = response.json()

    # Extract user_ids from the response
    user_ids = [item["user_id"] for item in data]
    print("User IDs:", user_ids)

    preceptors = []
    for user_id in user_ids:
        preceptor = db.query(User).filter(User.id == user_id).first()
        preceptors.append(preceptor)

    preceptor_data = [UserOut.from_orm(p) for p in preceptors]

    return APIResponse(
        status="00",
        message="Possible preceptor matches returned",
        data=preceptor_data
    )


def get_background(user_id: int, db: Session = Depends(get_db)):

    print("Retrieving background information for user_id: ", user_id)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    # Concatenate fields into a single string following the structure
    background_str = (
        f"Clinical Background: {user.clinical_background}\n\n"
        f"Learning Style: {user.learning_style}\n\n"
        f"Personality: {user.personality}\n\n"
        f"UserID: {user.id}"
    )

    return background_str

def match_orientee_with_perceptor(request: MatchRetrieve, db: Session):
    preceptor = db.query(User).filter(User.id == request.preceptor_id).first()

    if not preceptor:
        return {"error": "Preceptor not found"}

    # Create Match model
    new_match = Match(
        orientee_id=request.orientee_id,
        preceptor_id=request.preceptor_id,
    )

    db.add(new_match)
    db.commit()
    db.flush()

    return APIResponse(
        status="00",
        message="Orientee successfully matched with Preceptor",
        data=request.preceptor_id
    )