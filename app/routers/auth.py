from fastapi import APIRouter, Depends, HTTPException, status
from firebase_admin import auth
from typing import Optional

router = APIRouter()

@router.get("/verify-token")
def verify_token(id_token: str):
    """
    The front end calls this endpoint with a Firebase ID token.
    Example: GET /api/auth/verify-token?id_token=<TOKEN>
    """
    try:
        decoded_token = auth.verify_id_token(id_token)
        user_id = decoded_token["uid"]  # Firebase's unique user ID
        return {"uid": user_id, "status": "Token is valid"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
