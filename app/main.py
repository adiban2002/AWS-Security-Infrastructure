import logging
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from app.utils.config import settings


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

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


@app.get("/", include_in_schema=False)
async def serve_ui():
    index_path = os.path.join(FRONTEND_DIR, "index.html")
    return FileResponse(index_path)


app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")


from app.routes.routes import router
app.include_router(router)


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}