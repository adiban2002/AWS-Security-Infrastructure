from fastapi import APIRouter, HTTPException, Depends
from .service import create_user, get_user

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/")
def create(user_id: str, name: str):
    return create_user(user_id, name)

@router.get("/{user_id}") 
def fetch(user_id: str):
    try:
        user = get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found in Aurora DB")
        return user
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"Database internal error: {str(e)}"
        )