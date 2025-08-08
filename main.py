#!/usr/bin/env python3
"""
Main entry point for GitHub README Searcher API Server
"""

import uvicorn
import logging
from app.api.app import app
from app.config.settings import settings

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the API server"""
    logger.info(f"Starting GitHub README Searcher API v{settings.API_VERSION}")
    logger.info(f"Server will run on {settings.HOST}:{settings.PORT}")
    
    # Validate settings
    if not settings.validate():
        logger.warning("Some settings are not properly configured")
    
    # Start the server
    uvicorn.run(
        "app.api.app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )

if __name__ == "__main__":
    main() 