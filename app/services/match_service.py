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
        return APIResponse(
            status="01",
            message="Orientee not found"
        )

    data = UserOut.from_orm(orientee)
    if not data.type == "ORIENTEE":
        return APIResponse(
            status="01",
            message="User not an orientee"
        )


    background = get_background(orientee_id, db)
    payload = {"background": background}
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(settings.MATCH_URL, data=json.dumps(payload), headers=headers)
    if response.status_code != 200:
        return APIResponse(
            status="01",
            message="Failed to match orientee",
        )

    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", json.dumps(response.json(), indent=4))
    except Exception:
        print("Response Text:", response.text)

    # Convert response to JSON
    data = response.json()

    preceptors = []
    for item in data:
        preceptor = db.query(User).filter(User.id == item["user_id"]).first()
        if preceptor:
            preceptor_data = UserOut.from_orm(preceptor).dict()
            preceptor_data["match_information"] = item["information"]
            preceptors.append(preceptor_data)

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
        f"Name: {user.first_name}, {user.last_name}\n\n"
        f"Clinical Background: {user.clinical_background}\n\n"
        f"Learning Style: {user.learning_style}\n\n"
        f"Personality: {user.personality}\n\n"
        f"UserID: {user.id}"
    )

    return background_str

def match_orientee_with_perceptor(request: MatchRetrieve, db: Session):
    preceptor = db.query(User).filter(User.id == request.preceptor_id).first()
    orientee = db.query(User).filter(User.id == request.orientee_id).first()

    if not preceptor or not orientee:
        return APIResponse(
            status="01",
            message="Preceptor/Orientee not found"
        )

    orientee_data = UserOut.from_orm(orientee)
    preceptor_data = UserOut.from_orm(preceptor)

    if not orientee_data.type == "ORIENTEE":
        return APIResponse(
            status="01",
            message="User not an orientee"
        )

    if not preceptor_data.type == "PRECEPTOR":
        return APIResponse(
            status="01",
            message="User not a preceptor"
        )


    if orientee_data.matched:
        return APIResponse(
            status="01",
            message="Orientee already matched to a preceptor"
        )

    # Create Match model
    new_match = Match(
        orientee_id=request.orientee_id,
        preceptor_id=request.preceptor_id,
    )
    db.add(new_match)
    db.commit()
    db.flush()

    orientee.matched = True
    db.commit()
    db.refresh(orientee)


    return APIResponse(
        status="00",
        message="Orientee successfully matched with Preceptor",
        data=request.preceptor_id
    )