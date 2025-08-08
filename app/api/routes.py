"""
API routes for GitHub README Searcher
"""

import logging
from typing import List
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse

from app.core.models import (
    SearchRequest, SearchResponse, RepositoryResponse, 
    HealthResponse, StatsResponse
)
from app.core.searcher import GitHubAPISearcher
from app.config.settings import settings

logger = logging.getLogger(__name__)

# Create router
router = APIRouter()

# Simple statistics tracking (in production, use a proper database)
_search_stats = {
    "total_searches": 0,
    "total_repositories_found": 0,
    "searched_domains": {}
}


@router.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "GitHub README Searcher API - Direct Version",
        "version": settings.API_VERSION,
        "port": settings.PORT,
        "endpoints": {
            "search": "/search?keywords=python&limit=2",
            "search_path": "/search/{domain}?limit=2",
            "health": "/health",
            "domains": "/domains",
            "stats": "/stats",
            "docs": "/docs"
        }
    }


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    github_token_configured = bool(settings.GITHUB_TOKEN)
    
    # Test GitHub API connection if token is available
    api_connected = False
    if github_token_configured:
        try:
            async with GitHubAPISearcher() as searcher:
                # Try a simple search to test connection
                repos = await searcher.search_repositories("test", limit=1)
                api_connected = True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            api_connected = False
    
    return HealthResponse(
        status="healthy" if github_token_configured else "unhealthy",
        api_connected=api_connected,
        github_token_configured=github_token_configured
    )


@router.post("/search", response_model=SearchResponse)
async def search_repositories(request: SearchRequest):
    """Search repositories with README content"""
    try:
        async with GitHubAPISearcher() as searcher:
            repositories = await searcher.search_and_get_readmes(
                domain=request.domain,
                limit=request.limit
            )
            
            # Update statistics
            _search_stats["total_searches"] += 1
            _search_stats["total_repositories_found"] += len(repositories)
            _search_stats["searched_domains"][request.domain] = _search_stats["searched_domains"].get(request.domain, 0) + 1
            
            # Convert to response models
            repo_responses = [
                RepositoryResponse(
                    name=repo.name,
                    full_name=repo.full_name,
                    description=repo.description,
                    stars=repo.stars,
                    language=repo.language,
                    url=repo.url,
                    readme_content=repo.readme_content
                )
                for repo in repositories
            ]
            
            return SearchResponse(
                domain=request.domain,
                repositories=repo_responses,
                total_count=len(repo_responses)
            )
            
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/search")
async def search_repositories_query(
    keywords: str = Query(..., description="Search keywords"),
    limit: int = Query(default=5, ge=1, le=100, description="Maximum number of repositories")
):
    """Search repositories using query parameters"""
    try:
        async with GitHubAPISearcher() as searcher:
            repositories = await searcher.search_and_get_readmes(
                domain=keywords,
                limit=limit
            )
            
            # Update statistics
            _search_stats["total_searches"] += 1
            _search_stats["total_repositories_found"] += len(repositories)
            _search_stats["searched_domains"][keywords] = _search_stats["searched_domains"].get(keywords, 0) + 1
            
            return {
                "domain": keywords,
                "repositories": [
                    {
                        "name": repo.name,
                        "full_name": repo.full_name,
                        "description": repo.description,
                        "stars": repo.stars,
                        "language": repo.language,
                        "url": repo.url,
                        "readme_content": repo.readme_content
                    }
                    for repo in repositories
                ],
                "total_count": len(repositories)
            }
            
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/search/{domain}")
async def search_repositories_simple(
    domain: str,
    limit: int = Query(default=5, ge=1, le=100, description="Maximum number of repositories")
):
    """Simple search by domain path parameter"""
    try:
        async with GitHubAPISearcher() as searcher:
            repositories = await searcher.search_and_get_readmes(
                domain=domain,
                limit=limit
            )
            
            # Update statistics
            _search_stats["total_searches"] += 1
            _search_stats["total_repositories_found"] += len(repositories)
            _search_stats["searched_domains"][domain] = _search_stats["searched_domains"].get(domain, 0) + 1
            
            return {
                "domain": domain,
                "repositories": [
                    {
                        "name": repo.name,
                        "full_name": repo.full_name,
                        "description": repo.description,
                        "stars": repo.stars,
                        "language": repo.language,
                        "url": repo.url,
                        "readme_content": repo.readme_content
                    }
                    for repo in repositories
                ],
                "total_count": len(repositories)
            }
            
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/search/{domain}/no-readme")
async def search_repositories_no_readme(
    domain: str,
    limit: int = Query(default=5, ge=1, le=100, description="Maximum number of repositories")
):
    """Search repositories without README content (faster)"""
    try:
        async with GitHubAPISearcher() as searcher:
            repositories = await searcher.search_repositories(
                domain=domain,
                limit=limit
            )
            
            # Update statistics
            _search_stats["total_searches"] += 1
            _search_stats["total_repositories_found"] += len(repositories)
            _search_stats["searched_domains"][domain] = _search_stats["searched_domains"].get(domain, 0) + 1
            
            return {
                "domain": domain,
                "repositories": [
                    {
                        "name": repo.name,
                        "full_name": repo.full_name,
                        "description": repo.description,
                        "stars": repo.stars,
                        "language": repo.language,
                        "url": repo.url,
                        "readme_content": None
                    }
                    for repo in repositories
                ],
                "total_count": len(repositories)
            }
            
    except Exception as e:
        logger.error(f"Search error: {e}")
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/domains")
async def get_popular_domains():
    """Get popular search domains"""
    popular_domains = [
        "machine learning",
        "artificial intelligence", 
        "web development",
        "mobile development",
        "data science",
        "blockchain",
        "cybersecurity",
        "devops",
        "react",
        "vue",
        "angular",
        "python",
        "javascript",
        "typescript",
        "go",
        "rust",
        "docker",
        "kubernetes",
        "microservices",
        "api development",
        "database",
        "cloud computing",
        "serverless",
        "game development",
        "computer vision",
        "natural language processing",
        "deep learning"
    ]
    
    return {
        "popular_domains": popular_domains,
        "total_count": len(popular_domains),
        "description": "Popular technology domains for GitHub repository search"
    }


@router.get("/stats", response_model=StatsResponse)
async def get_api_stats():
    """Get API usage statistics"""
    total_searches = _search_stats["total_searches"]
    total_repositories = _search_stats["total_repositories_found"]
    
    # Calculate average repositories per search
    average_repos = total_repositories / total_searches if total_searches > 0 else 0
    
    # Get most searched domains
    sorted_domains = sorted(
        _search_stats["searched_domains"].items(),
        key=lambda x: x[1],
        reverse=True
    )
    most_searched = [domain for domain, count in sorted_domains[:10]]
    
    return StatsResponse(
        total_searches=total_searches,
        total_repositories_found=total_repositories,
        average_repositories_per_search=round(average_repos, 2),
        most_searched_domains=most_searched
    ) 