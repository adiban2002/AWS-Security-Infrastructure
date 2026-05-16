from sqlalchemy import Column, String
from app.utils.db_config import Base

class User(Base):
    __tablename__ = "users"
    user_id = Column(String(50), primary_key=True)
    name = Column(String(100))

def create_user(user_id: str, name: str):
    try:
        from app.utils.db_config import SessionLocal
        
        with SessionLocal() as db:
            new_user = User(user_id=user_id, name=name)
            db.add(new_user)
            db.commit()
            return {"user_id": user_id, "name": name, "status": "created"}
    except Exception as e:
        raise Exception(f"Database insert failed: {str(e)}")

def get_user(user_id: str):
    try:
        from app.utils.db_config import SessionLocal
        
        with SessionLocal() as db:
            return db.query(User).filter(User.user_id == user_id).first()
    except Exception as e:
        raise Exception(f"Database query failed: {str(e)}")