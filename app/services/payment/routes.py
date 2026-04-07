from fastapi import APIRouter
from .service import create_payment

router = APIRouter(prefix="/payment", tags=["Payment"])

@router.post("/")
def pay(user_id: str, amount: float):
    return create_payment(user_id, amount)