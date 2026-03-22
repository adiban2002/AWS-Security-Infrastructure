import os
from functools import lru_cache


class Settings:
    APP_NAME: str = os.getenv("APP_NAME", "DevSecOps Secure API")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "True") == "True"

    AWS_REGION: str = os.getenv("AWS_REGION", "ap-south-1")

    PARAMETER_PREFIX: str = os.getenv("PARAMETER_PREFIX", "/devsecops/app")

    SECRET_NAME: str = os.getenv("SECRET_NAME", "devsecops/secret")

    API_KEY: str = os.getenv("API_KEY", "changeme")

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()