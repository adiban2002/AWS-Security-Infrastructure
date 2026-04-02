import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.routes.routes import router
from app.utils.config import settings

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting DevSecOps Application...")
    yield
    logger.info("Shutting down application...")

app = FastAPI(
    title="DevSecOps Secure Cloud API",
    version="1.0.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)

@app.get("/", tags=["Health"])
def root():
    return {
        "status": "running",
        "service": settings.APP_NAME,
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}