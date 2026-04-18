import os
from config_management.parameter_store import ssm_manager
from config_management.secrets_manager import secrets_provider


print("Fetching DB configurations from AWS...")
DB_ENDPOINT = ssm_manager.get_parameter("/findmyproject/db_endpoint")

db_creds = secrets_provider.get_secret("findmyproject/db_creds")

if db_creds:
    DB_USER = db_creds.get('username')
    DB_PASSWORD = db_creds.get('password')
else:
    raise Exception("Could not retrieve DB credentials from Secrets Manager")

DB_NAME = "devsecops_db" 
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_ENDPOINT}/{DB_NAME}"

print("DB Configuration loaded successfully from Cloud.")