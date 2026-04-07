from fastapi import APIRouter, HTTPException
from .service import generate_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
def login(user_id: str):
    token = generate_token(user_id)
    return {"access_token": token}