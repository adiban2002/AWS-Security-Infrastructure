from app.utils.db_config import SessionLocal, Base, engine
from sqlalchemy import Column, String

class User(Base):
    __tablename__ = "users"
    user_id = Column(String(50), primary_key=True)
    name = Column(String(100))

# টেবিল তৈরি করা
Base.metadata.create_all(bind=engine)

# নতুন ইউজার তৈরি করার ফাংশন
def create_user(user_id: str, name: str):
    with SessionLocal() as db:
        new_user = User(user_id=user_id, name=name)
        db.add(new_user)
        db.commit()
        return {"user_id": user_id, "name": name}

# এই ফাংশনটি মিসিং ছিল, এখন যোগ করে দিলাম
def get_user(user_id: str):
    with SessionLocal() as db:
        return db.query(User).filter(User.user_id == user_id).first()