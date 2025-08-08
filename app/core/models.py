"""
Data models for GitHub README Searcher
"""

from dataclasses import dataclass
from typing import Optional, List
from pydantic import BaseModel, Field


@dataclass
class RepositoryInfo:
    """Repository information data class"""
    name: str
    full_name: str
    description: str
    stars: int
    language: str
    url: str
    readme_content: Optional[str] = None


# Pydantic models for API requests and responses
class SearchRequest(BaseModel):
    """Search request model"""
    domain: str = Field(..., description="Domain/topic to search for (e.g., 'machine learning', 'web development')")
    limit: int = Field(default=5, ge=1, le=100, description="Maximum number of repositories to return")


class RepositoryResponse(BaseModel):
    """Repository response model"""
    name: str
    full_name: str
    description: str
    stars: int
    language: str
    url: str
    readme_content: Optional[str] = None


class SearchResponse(BaseModel):
    """Search response model"""
    domain: str
    repositories: List[RepositoryResponse]
    total_count: int


class HealthResponse(BaseModel):
    """Health check response model"""
    status: str
    api_connected: bool
    github_token_configured: bool


class StatsResponse(BaseModel):
    """API statistics response model"""
    total_searches: int
    total_repositories_found: int
    average_repositories_per_search: float
    most_searched_domains: List[str] 