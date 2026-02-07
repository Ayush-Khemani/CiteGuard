"""
Main FastAPI application for CiteGuard.
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.api.routes import analysis, auth, documents, sources

# Configure logging
logging.basicConfig(
    level=settings.LOG_LEVEL,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    # Startup
    logger.info("Starting CiteGuard API...")
    logger.info(f"Debug mode: {settings.DEBUG}")
    
    # Initialize ML models on startup for faster first request
    try:
        from app.services.similarity import get_similarity_service
        logger.info("Loading similarity detection model...")
        get_similarity_service()
        logger.info("✓ Similarity model loaded")
    except Exception as e:
        logger.error(f"Failed to load similarity model: {e}")
    
    yield
    
    # Shutdown
    logger.info("Shutting down CiteGuard API...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Academic plagiarism prevention API - helping students write with integrity",
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "service": settings.APP_NAME
    }


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to CiteGuard API",
        "version": settings.APP_VERSION,
        "docs": "/docs" if settings.DEBUG else "Documentation disabled in production",
        "endpoints": {
            "health": "/health",
            "auth": f"{settings.API_V1_PREFIX}/auth",
            "analysis": f"{settings.API_V1_PREFIX}/analysis",
            "documents": f"{settings.API_V1_PREFIX}/documents",
            "sources": f"{settings.API_V1_PREFIX}/sources",
        }
    }


# Include API routers
app.include_router(
    auth.router,
    prefix=f"{settings.API_V1_PREFIX}/auth",
    tags=["Authentication"]
)

app.include_router(
    analysis.router,
    prefix=f"{settings.API_V1_PREFIX}/analysis",
    tags=["Analysis"]
)

app.include_router(
    documents.router,
    prefix=f"{settings.API_V1_PREFIX}/documents",
    tags=["Documents"]
)

app.include_router(
    sources.router,
    prefix=f"{settings.API_V1_PREFIX}/sources",
    tags=["Sources"]
)


# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An unexpected error occurred",
            "type": "internal_server_error"
        }
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )