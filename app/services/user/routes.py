from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from .service import create_user, get_user

router = APIRouter(prefix="/user", tags=["User"])

class UserCreate(BaseModel):
    user_id: str
    name: str

@router.post("/")
def create(user_data: UserCreate):
    try:
        return create_user(user_id=user_data.user_id, name=user_data.name)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{user_id}")
def fetch(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found in Aurora DB")
    return user