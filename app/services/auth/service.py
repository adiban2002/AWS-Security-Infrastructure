import jwt
from datetime import datetime, timedelta, timezone
from app.utils.config import settings

SECRET = settings.API_KEY

def generate_token(user_id: str):
    payload = {
        "sub": user_id,
        "exp": datetime.now(timezone.utc) + timedelta(hours=2)
    }
    return jwt.encode(payload, SECRET, algorithm="HS256")


def verify_token(token: str):
    try:
        decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
        return decoded
    except Exception:
        return None