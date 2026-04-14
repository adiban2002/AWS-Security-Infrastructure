import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DB_ENDPOINT = "devsecops-db-auroradbcluster-uecwzdckzkov.cluster-cdso4micm2ww.ap-south-1.rds.amazonaws.com"
DB_NAME = "security_infrastructure_db" 
DB_USER = "db_admin"
DB_PASS = "Complex_Sec_99_Auth" 
DATABASE_URL = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_ENDPOINT}/{DB_NAME}"
engine = create_engine(
    DATABASE_URL, 
    pool_size=10, 
    max_overflow=20,
    pool_pre_ping=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    print(f"--- DevSecOps Infrastructure DB Configuration ---")
    print(f"Host: {DB_ENDPOINT}")
    print(f"Status: Configured for Aditya Banerjee")