from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from app.routes.routes import router

logging.basicConfig(
    level=logging.INFO,
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
    description="Production-ready FastAPI service with AWS integration",
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
def health_check():
    return {
        "status": "running",
        "service": "DevSecOps Secure API",
        "version": "1.0.0",
    }


@app.get("/health", tags=["Health"])
def readiness_probe():
    return {"status": "healthy"}


@app.get("/live", tags=["Health"])
def liveness_probe():
    return {"status": "alive"}