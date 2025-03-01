from firebase_admin import firestore
from app.schemas.user import UserProfile
import uuid

db = firestore.client()

def create_user_in_firestore(user_data: UserProfile):
    # Generate a doc ID or use something from user_data
    doc_id = str(uuid.uuid4())
    user_dict = user_data.dict()
    db.collection("users").document(doc_id).set(user_dict)
    return doc_id


