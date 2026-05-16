import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.db_config import engine, Base
from app.services.user.service import User 

def create_tables():
    print("Connecting to Aurora DB Cluster using admin credentials...")
    try:
        Base.metadata.create_all(bind=engine)
        print("Success! 'users' table has been created successfully in Aurora DB!")
    except Exception as e:
        print(f"Error during table creation: {str(e)}")

if __name__ == "__main__":
    create_tables()