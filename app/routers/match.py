from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.match import MatchRetrieve
from app.services.match_service import retrieve_all_possible_matches, match_orientee_with_perceptor

router = APIRouter()


@router.get("/retrieve/{orientee_id}")
def retrieve_possible_matches(
        orientee_id: int,
        db: Session = Depends(get_db)
        # current_user: dict = Depends(verify_firebase_token)
):
    return retrieve_all_possible_matches(orientee_id, db)

@router.post("")
def perform_match(
        request: MatchRetrieve,
        db: Session = Depends(get_db)
        # current_user: dict = Depends(verify_firebase_token)
):
    return match_orientee_with_perceptor(request, db)