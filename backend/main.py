from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes import router
from config.settings import settings
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="AI Video Studio API",
    description="Complete free YouTube automation platform using Groq, Edge-TTS, and MoviePy",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router)

# Ensure output directories exist
os.makedirs(settings.OUTPUT_PATH, exist_ok=True)
os.makedirs(settings.TEMP_PATH, exist_ok=True)

# Mount static files for serving videos
if os.path.exists(settings.OUTPUT_PATH):
    app.mount(
        "/api/v1/videos",
        StaticFiles(directory=settings.OUTPUT_PATH),
        name="videos"
    )


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info("🎬 AI Video Studio API starting up...")
    logger.info(f"Environment: {settings.APP_ENV}")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Output path: {settings.OUTPUT_PATH}")
    logger.info(f"Temp path: {settings.TEMP_PATH}")
    logger.info(f"Groq API configured: {'Yes' if settings.GROQ_API_KEY else 'No'}")
    logger.info("✅ API is ready!")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info("🛑 AI Video Studio API shutting down...")


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "🎬 Welcome to AI Video Studio API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": f"{settings.API_V1_PREFIX}/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )
