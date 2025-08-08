"""
GitHub API Searcher - Core search functionality

This module provides a direct interface to GitHub API for searching repositories
and retrieving README content without requiring MCP or Docker.
"""

import asyncio
import aiohttp
import logging
from typing import List, Optional
from urllib.parse import quote

from app.core.models import RepositoryInfo
from app.config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)


class GitHubAPISearcher:
    """GitHub API Searcher for finding repositories and retrieving README content"""
    
    def __init__(self, github_token: Optional[str] = None, github_host: Optional[str] = None):
        self.github_token = github_token or settings.GITHUB_TOKEN
        self.github_host = (github_host or settings.GITHUB_HOST).rstrip('/')
        self.session = None
        
        if not self.github_token:
            raise ValueError("GitHub token is required")
        
    async def __aenter__(self):
        """Async context manager entry"""
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-README-Searcher/2.0.0'
        }
        
        self.session = aiohttp.ClientSession(headers=headers)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def search_repositories(self, domain: str, limit: int = 5) -> List[RepositoryInfo]:
        """
        Search for repositories in a specific domain
        
        Args:
            domain: Domain/topic to search for
            limit: Maximum number of repositories to return
            
        Returns:
            List of RepositoryInfo objects
        """
        # Build search query - search by domain and sort by stars
        query = f'{domain} sort:stars'
        
        # GitHub API allows max 100 items per page, so we need to handle pagination
        # to get enough repositories to sort by stars
        all_repos = []
        page = 1
        per_page = min(100, limit * 2)  # Get more than needed to ensure we have enough after sorting
        
        while len(all_repos) < limit * 2 and page <= 3:  # Limit to 3 pages to avoid too many requests
            url = f"{self.github_host}/search/repositories"
            params = {
                'q': query,
                'sort': 'stars',
                'order': 'desc',
                'per_page': per_page,
                'page': page
            }
            
            try:
                async with self.session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        repos = data.get('items', [])
                        all_repos.extend(repos)
                        
                        # If we got fewer results than requested, we've reached the end
                        if len(repos) < per_page:
                            break
                    else:
                        error_text = await response.text()
                        logger.error(f"GitHub API error: {response.status} - {error_text}")
                        break
                        
            except Exception as e:
                logger.error(f"Error searching repositories: {e}")
                break
                
            page += 1
        
        # Convert to RepositoryInfo objects and limit results
        repository_infos = []
        for repo in all_repos[:limit]:
            repository_info = RepositoryInfo(
                name=repo['name'],
                full_name=repo['full_name'],
                description=repo.get('description', ''),
                stars=repo.get('stargazers_count', 0),
                language=repo.get('language', 'Unknown'),
                url=repo['html_url']
            )
            repository_infos.append(repository_info)
        
        return repository_infos
    
    async def get_readme_content(self, owner: str, repo: str) -> Optional[str]:
        """
        Get README content for a specific repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            README content as string, or None if not found
        """
        url = f"{self.github_host}/repos/{owner}/{repo}/readme"
        
        try:
            async with self.session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    content = data.get('content', '')
                    encoding = data.get('encoding', 'base64')
                    
                    if encoding == 'base64':
                        import base64
                        return base64.b64decode(content).decode('utf-8')
                    else:
                        return content
                else:
                    logger.warning(f"Could not get README for {owner}/{repo}: {response.status}")
                    return None
                    
        except Exception as e:
            logger.error(f"Error getting README for {owner}/{repo}: {e}")
            return None
    
    async def search_and_get_readmes(self, domain: str, limit: int = 5) -> List[RepositoryInfo]:
        """
        Search for repositories and get their README content
        
        Args:
            domain: Domain/topic to search for
            limit: Maximum number of repositories to return
            
        Returns:
            List of RepositoryInfo objects with README content
        """
        # First, search for repositories
        repositories = await self.search_repositories(domain, limit)
        
        # Then, get README content for each repository
        tasks = []
        for repo in repositories:
            owner, repo_name = repo.full_name.split('/', 1)
            task = self.get_readme_content(owner, repo_name)
            tasks.append((repo, task))
        
        # Execute all README requests concurrently
        for repo, task in tasks:
            try:
                readme_content = await task
                repo.readme_content = readme_content
            except Exception as e:
                logger.error(f"Error getting README for {repo.full_name}: {e}")
                repo.readme_content = None
        
        return repositories 