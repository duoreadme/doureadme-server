"""
Application settings and configuration
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application settings"""
    
    # GitHub API Configuration
    GITHUB_TOKEN: Optional[str] = os.getenv('GITHUB_TOKEN')
    GITHUB_HOST: str = os.getenv('GITHUB_HOST', 'https://api.github.com')
    
    # Server Configuration
    HOST: str = os.getenv('HOST', '0.0.0.0')
    PORT: int = int(os.getenv('PORT', '5088'))
    DEBUG: bool = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # API Configuration
    API_TITLE: str = "GitHub README Searcher API"
    API_DESCRIPTION: str = "API for searching GitHub repositories and retrieving README content"
    API_VERSION: str = "2.0.0"
    
    # Search Configuration
    DEFAULT_SEARCH_LIMIT: int = 5
    MAX_SEARCH_LIMIT: int = 100
    DEFAULT_README_LENGTH: int = 500
    
    # CORS Configuration
    CORS_ORIGINS: list = ["*"]
    CORS_METHODS: list = ["*"]
    CORS_HEADERS: list = ["*"]
    
    # Logging Configuration
    LOG_LEVEL: str = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls) -> bool:
        """Validate required settings"""
        if not cls.GITHUB_TOKEN:
            print("Warning: GITHUB_TOKEN not set. Some features may not work.")
            return False
        return True

# Global settings instance
settings = Settings() 