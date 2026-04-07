def send_notification(user_id: str, message: str):
    return {
        "user_id": user_id,
        "message": message,
        "status": "sent"
    }