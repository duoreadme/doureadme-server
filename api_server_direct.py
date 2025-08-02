#!/usr/bin/env python3
"""
FastAPI Server for GitHub README Searcher - Direct API Version

Provides REST API endpoints to search GitHub repositories and retrieve README content
using direct GitHub API calls (no MCP or Docker required).
"""

import asyncio
import os
from typing import List, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from github_api_searcher import GitHubAPISearcher, RepositoryInfo

# Load environment variables
load_dotenv()

# Pydantic models for API requests and responses
class SearchRequest(BaseModel):
    domain: str = Field(..., description="Domain/topic to search for (e.g., 'machine learning', 'web development')")
    limit: int = Field(default=5, ge=1, le=100, description="Maximum number of repositories to return")

class RepositoryResponse(BaseModel):
    name: str
    full_name: str
    description: str
    stars: int
    language: str
    url: str
    readme_content: Optional[str] = None

class SearchResponse(BaseModel):
    domain: str
    repositories: List[RepositoryResponse]
    total_count: int

class HealthResponse(BaseModel):
    status: str
    api_connected: bool
    github_token_configured: bool

# Create FastAPI app
app = FastAPI(
    title="GitHub README Searcher API",
    description="API for searching GitHub repositories and retrieving README content using direct GitHub API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "GitHub README Searcher API - Direct Version",
        "version": "2.0.0",
        "port": 5088,
        "endpoints": {
            "search": "/search?keywords=python&limit=2",
            "search_path": "/search/{domain}?limit=2",
            "health": "/health",
            "domains": "/domains",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    github_token = os.getenv('GITHUB_TOKEN')
    github_token_configured = bool(github_token)
    
    # Test GitHub API connection if token is available
    api_connected = False
    if github_token_configured:
        try:
            async with GitHubAPISearcher(github_token) as searcher:
                # Try a simple search to test connection
                repos = await searcher.search_repositories("test", limit=1)
                api_connected = True
        except Exception:
            api_connected = False
    
    return HealthResponse(
        status="healthy" if github_token_configured else "unhealthy",
        api_connected=api_connected,
        github_token_configured=github_token_configured
    )

@app.post("/search", response_model=SearchResponse)
async def search_repositories(request: SearchRequest):
    """
    Search for repositories in a specific domain and retrieve README content
    
    Args:
        request: Search parameters including domain and limit
        
    Returns:
        SearchResponse with repository information and README content
    """
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise HTTPException(status_code=503, detail="GitHub token not configured")
    
    try:
        # Use async context manager
        async with GitHubAPISearcher(github_token) as searcher:
            # Search for repositories and get README content
            repositories = await searcher.search_and_get_readmes(
                domain=request.domain,
                limit=request.limit
            )
            
            # Convert to response format
            repo_responses = []
            for repo in repositories:
                repo_response = RepositoryResponse(
                    name=repo.name,
                    full_name=repo.full_name,
                    description=repo.description,
                    stars=repo.stars,
                    language=repo.language,
                    url=repo.url,
                    readme_content=repo.readme_content
                )
                repo_responses.append(repo_response)
            
            return SearchResponse(
                domain=request.domain,
                repositories=repo_responses,
                total_count=len(repo_responses)
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/search")
async def search_repositories_query(
    keywords: str,
    limit: int = 5
):
    """
    Search endpoint using query parameters
    
    Args:
        keywords: Keywords/topic to search for
        limit: Maximum number of repositories (query parameter)
        
    Returns:
        Search results
    """
    request = SearchRequest(domain=keywords, limit=limit)
    return await search_repositories(request)

@app.get("/search/{domain}")
async def search_repositories_simple(
    domain: str,
    limit: int = 5
):
    """
    Simple search endpoint using path parameters
    
    Args:
        domain: Domain/topic to search for
        limit: Maximum number of repositories (query parameter)
        
    Returns:
        Search results
    """
    request = SearchRequest(domain=domain, limit=limit)
    return await search_repositories(request)

@app.get("/search/{domain}/no-readme")
async def search_repositories_no_readme(
    domain: str,
    limit: int = 5
):
    """
    Search repositories without retrieving README content (faster)
    
    Args:
        domain: Domain/topic to search for
        limit: Maximum number of repositories (query parameter)
        
    Returns:
        Search results without README content
    """
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        raise HTTPException(status_code=503, detail="GitHub token not configured")
    
    try:
        async with GitHubAPISearcher(github_token) as searcher:
            # Search for repositories only (no README)
            repositories = await searcher.search_repositories(
                domain=domain,
                limit=limit
            )
            
            # Convert to response format
            repo_responses = []
            for repo in repositories:
                repo_response = RepositoryResponse(
                    name=repo.name,
                    full_name=repo.full_name,
                    description=repo.description,
                    stars=repo.stars,
                    language=repo.language,
                    url=repo.url,
                    readme_content=None
                )
                repo_responses.append(repo_response)
            
            return SearchResponse(
                domain=domain,
                repositories=repo_responses,
                total_count=len(repo_responses)
            )
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")

@app.get("/domains")
async def get_popular_domains():
    """Get list of popular domains for search suggestions"""
    return {
        "popular_domains": [
            "machine learning",
            "artificial intelligence",
            "web development",
            "mobile development",
            "data science",
            "blockchain",
            "cybersecurity",
            "devops",
            "frontend",
            "backend",
            "full stack",
            "react",
            "vue",
            "angular",
            "python",
            "javascript",
            "typescript",
            "go",
            "rust",
            "kubernetes",
            "docker",
            "microservices",
            "api",
            "database",
            "cloud computing",
            "serverless",
            "game development",
            "computer vision",
            "natural language processing",
            "deep learning"
        ]
    }

@app.get("/stats")
async def get_api_stats():
    """Get API usage statistics"""
    return {
        "api_version": "2.0.0",
        "port": 5088,
        "features": [
            "Direct GitHub API integration",
            "No Docker required",
            "Async processing",
            "README content retrieval",
            "Flexible search parameters",
            "CORS enabled",
            "OpenAPI documentation",
            "Sort by stars (descending)"
        ],
        "endpoints": {
            "search": "GET /search?keywords=python&limit=2 - Search with query parameters",
            "search_post": "POST /search - Full search with README (request body)",
            "search_path": "GET /search/{domain} - Simple search with path parameters",
            "search_fast": "GET /search/{domain}/no-readme - Fast search without README",
            "health": "GET /health - Health check",
            "domains": "GET /domains - Popular domains list",
            "docs": "GET /docs - API documentation"
        }
    }

if __name__ == "__main__":
    import uvicorn
    
    # Check for required environment variable
    if not os.getenv('GITHUB_TOKEN'):
        print("Warning: GITHUB_TOKEN environment variable is not set")
        print("Please set it with: export GITHUB_TOKEN=your_github_token")
        print("Or create a .env file with: GITHUB_TOKEN=your_github_token")
        print("The API will still start but search endpoints will return errors.")
    
    # Run the server on port 5088
    print("Starting GitHub README Searcher API Server...")
    print("Server will be available at: http://localhost:5088")
    print("API documentation: http://localhost:5088/docs")
    print("Health check: http://localhost:5088/health")
    
    uvicorn.run(
        "api_server_direct:app",
        host="0.0.0.0",
        port=5088,
        reload=True,
        log_level="info"
    ) 