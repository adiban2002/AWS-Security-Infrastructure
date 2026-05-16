import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from app.utils.config import settings

BASE_DIR = os.getcwd() 
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL, "INFO"),
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("app")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting DevSecOps Application...")
    logger.info(f"Checking Frontend Path: {FRONTEND_DIR}")
    if os.path.exists(FRONTEND_DIR):
        logger.info("Frontend directory found!")
    else:
        logger.error("Frontend directory NOT FOUND inside container!")
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

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}


from app.routes.routes import router as api_router
app.include_router(api_router)


@app.get("/", include_in_schema=False)
async def serve_ui():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    return {
        "error": "Frontend build not found",
        "current_working_dir": BASE_DIR,
        "checked_path": index_path,
        "hint": "Ensure Dockerfile copies the frontend folder into /app/frontend"
    }

if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
else:
    logger.warning(f"Frontend directory not found at {FRONTEND_DIR}")