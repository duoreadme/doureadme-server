#!/usr/bin/env python3
"""
GitHub README Searcher - Direct API Version

This module provides a direct interface to GitHub API for searching repositories
and retrieving README content without requiring MCP or Docker.
"""

import asyncio
import aiohttp
import logging
from typing import List, Optional
from dataclasses import dataclass
from urllib.parse import quote

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class RepositoryInfo:
    """Repository information"""
    name: str
    full_name: str
    description: str
    stars: int
    language: str
    url: str
    readme_content: Optional[str] = None

class GitHubAPISearcher:
    """GitHub API Searcher for finding repositories and retrieving README content"""
    
    def __init__(self, github_token: str, github_host: str = "https://api.github.com"):
        self.github_token = github_token
        self.github_host = github_host.rstrip('/')
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json',
            'User-Agent': 'GitHub-README-Searcher/1.0'
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
        
        # Convert to RepositoryInfo objects and sort by stars (descending)
        repositories = []
        for repo in all_repos:
            repo_info = RepositoryInfo(
                name=repo['name'],
                full_name=repo['full_name'],
                description=repo.get('description', ''),
                stars=repo['stargazers_count'],
                language=repo.get('language', 'Unknown'),
                url=repo['html_url']
            )
            repositories.append(repo_info)
        
        # Sort by stars in descending order and take top N
        repositories.sort(key=lambda x: x.stars, reverse=True)
        repositories = repositories[:limit]
        
        logger.info(f"Found {len(repositories)} repositories for domain '{domain}'")
        return repositories
    
    async def get_readme_content(self, owner: str, repo: str) -> Optional[str]:
        """
        Get README content for a specific repository
        
        Args:
            owner: Repository owner
            repo: Repository name
            
        Returns:
            README content as string, or None if not found
        """
        # Try different README file names
        readme_files = ['README.md', 'README.rst', 'README.txt', 'README']
        
        for readme_file in readme_files:
            url = f"{self.github_host}/repos/{owner}/{repo}/contents/{readme_file}"
            
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        
                        # Get the download URL for the content
                        download_url = data.get('download_url')
                        if download_url:
                            async with self.session.get(download_url) as content_response:
                                if content_response.status == 200:
                                    content = await content_response.text()
                                    logger.info(f"Retrieved README for {owner}/{repo}")
                                    return content
                                    
            except Exception as e:
                logger.warning(f"Error getting README for {owner}/{repo}: {e}")
                continue
        
        logger.warning(f"No README found for {owner}/{repo}")
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