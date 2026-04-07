from fastapi import APIRouter, HTTPException
from .service import create_user, get_user

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/")
def create(user_id: str, name: str):
    return create_user(user_id, name)


@router.get("/{user_id}")
def fetch(user_id: str):
    user = get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user