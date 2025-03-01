from pydantic import BaseModel, EmailStr

class MatchRetrieve(BaseModel):
    orientee_id: int = None
    preceptor_id: int = None
    match_information: str = None