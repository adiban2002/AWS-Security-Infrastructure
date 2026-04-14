from app.utils.db_config import SessionLocal, Base, engine
from sqlalchemy import Column, String, Float
import uuid

class Payment(Base):
    __tablename__ = "payments"
    payment_id = Column(String(50), primary_key=True)
    user_id = Column(String(50))
    amount = Column(Float)

Base.metadata.create_all(bind=engine)

def create_payment(user_id: str, amount: float):
    with SessionLocal() as db:
        p_id = str(uuid.uuid4())
        new_payment = Payment(payment_id=p_id, user_id=user_id, amount=amount)
        db.add(new_payment)
        db.commit()
        return {"payment_id": p_id, "status": "success"}