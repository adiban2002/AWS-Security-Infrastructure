import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting DevSecOps Application...")
    logger.info(f"Checking Frontend Path: {FRONTEND_DIR}")
    if os.path.exists(FRONTEND_DIR):
        logger.info("Frontend directory found!")
    else:
        logger.error("Frontend directory NOT FOUND inside container!")
        
    
    try:
        from app.utils.db_config import init_db
        init_db()
    except Exception as e:
        logger.critical(f"Lifespan database initialization failed: {str(e)}")
        raise e
        
    yield
    logger.info("Shutting down application...")


app = FastAPI(lifespan=lifespan)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "devsecops-app"}


from app.routes.routes import router as api_router
app.include_router(api_router, prefix="/api/v1")


if os.path.exists(FRONTEND_DIR):
    app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
    
    @app.exception_handler(404)
    async def custom_404_handler(request, __):
        return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))
else:
    @app.get("/")
    def read_root():
        return {"message": "Welcome to DevSecOps Application. Frontend build missing."}