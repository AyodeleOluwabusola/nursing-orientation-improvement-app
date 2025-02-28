from fastapi import APIRouter, Depends
from app.services.firebase_auth import verify_firebase_token
from firebase_admin import firestore

router = APIRouter()
db = firestore.client()

@router.get("/secure-data")
def get_secure_data(decoded_token: dict = Depends(verify_firebase_token)):
    # If we reach here, the token is valid
    user_id = decoded_token.get("uid")
    return {"message": "Here is some secure data", "uid": user_id}
