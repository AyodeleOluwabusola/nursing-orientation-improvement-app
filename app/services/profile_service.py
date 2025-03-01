from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate

def create_user_profile(user_data: UserCreate, db: Session):

    new_user = User(
        email=user_data.email,
        type=user_data.type,
        clinical_background=user_data.clinical_background,
        learning_style=user_data.learning_style,
        personality=user_data.personality,
        academic_background=user_data.academic_background,
        specialty=user_data.specialty
    )
    db.add(new_user)
    db.commit()
    db.flush()

    print("ID Value: ", new_user.id)
    if (user_data.type == "PRECEPTOR"):
        # Call Vector database
        pass

    return UserCreate(
        email=new_user.email,
        academic_background= new_user.academic_background,
        clinical_background= new_user.clinical_background,
        learning_style= new_user.learning_style,
        personality= new_user.personality,
        type= new_user.type,
        specialty= new_user.specialty
    )