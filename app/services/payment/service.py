import uuid

payments_db = {}

def create_payment(user_id: str, amount: float):
    payment_id = str(uuid.uuid4())

    payment = {
        "payment_id": payment_id,
        "user_id": user_id,
        "amount": amount,
        "status": "completed"
    }

    payments_db[payment_id] = payment
    return payment