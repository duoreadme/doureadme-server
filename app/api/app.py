"""
FastAPI application for GitHub README Searcher
"""

import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app() -> FastAPI:
    """Create and configure FastAPI application"""
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.API_TITLE,
        description=settings.API_DESCRIPTION,
        version=settings.API_VERSION,
        docs_url="/docs",
        redoc_url="/redoc"
    )
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    
    # Include API routes
    app.include_router(router, prefix="/api/v1")
    
    # Add startup event
    @app.on_event("startup")
    async def startup_event():
        logger.info(f"Starting {settings.API_TITLE} v{settings.API_VERSION}")
        logger.info(f"Server will run on {settings.HOST}:{settings.PORT}")
        
        # Validate settings
        if not settings.validate():
            logger.warning("Some settings are not properly configured")
    
    # Add shutdown event
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("Shutting down GitHub README Searcher API")
    
    return app

# Create app instance
app = create_app() 