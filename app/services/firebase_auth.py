from fastapi import Request, HTTPException, status, Depends
from firebase_admin import auth

async def verify_firebase_token(request: Request):
    # For example, parse the 'Authorization' header
    auth_header: str = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid auth header")

    token = auth_header[len("Bearer "):]
    try:
        decoded_token = auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
