from fastapi import APIRouter
from .service import send_notification

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.post("/")
def notify(user_id: str, message: str):
    return send_notification(user_id, message)