import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config_management.parameter_store import ssm_manager
from config_management.secrets_manager import secrets_provider

print("Initializing DB configurations variables...")

engine = None
SessionLocal = None
Base = declarative_base()

def init_db():
    global engine, SessionLocal
    
    print("Fetching DB configurations from AWS with active IAM session...")
    
    try:
        DB_ENDPOINT = ssm_manager.get_parameter("/findmyproject/db_endpoint")
        db_creds = secrets_provider.get_secret("findmyproject/db_creds")
        
        if not db_creds:
            raise Exception("Secrets Manager returned empty credentials")
            
        DB_USER = db_creds.get('username')
        DB_PASSWORD = db_creds.get('password')
        DB_NAME = "devsecops_db"
        
        SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}"
        
        engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        
        print("DB Configuration loaded successfully from Cloud.")
    except Exception as e:
        print(f"CRITICAL: Failed to load DB configurations: {str(e)}")
        raise e