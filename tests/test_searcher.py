"""
Tests for GitHub API Searcher
"""

import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from app.core.searcher import GitHubAPISearcher
from app.core.models import RepositoryInfo


class TestGitHubAPISearcher:
    """Test cases for GitHubAPISearcher"""
    
    @pytest.fixture
    def mock_token(self):
        return "test_token"
    
    @pytest.fixture
    def searcher(self, mock_token):
        return GitHubAPISearcher(mock_token)
    
    def test_init_with_token(self, mock_token):
        """Test searcher initialization with token"""
        searcher = GitHubAPISearcher(mock_token)
        assert searcher.github_token == mock_token
        assert searcher.github_host == "https://api.github.com"
    
    def test_init_without_token(self):
        """Test searcher initialization without token"""
        with pytest.raises(ValueError, match="GitHub token is required"):
            GitHubAPISearcher(None)
    
    @pytest.mark.asyncio
    async def test_context_manager(self, searcher):
        """Test async context manager"""
        async with searcher as s:
            assert s.session is not None
            assert s.session.headers['Authorization'] == 'token test_token'
    
    @pytest.mark.asyncio
    async def test_search_repositories_success(self, searcher):
        """Test successful repository search"""
        mock_response_data = {
            'items': [
                {
                    'name': 'test-repo',
                    'full_name': 'test-owner/test-repo',
                    'description': 'Test repository',
                    'stargazers_count': 100,
                    'language': 'Python',
                    'html_url': 'https://github.com/test-owner/test-repo'
                }
            ]
        }
        
        with patch.object(searcher, 'session') as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_session.get.return_value.__aenter__.return_value = mock_response
            
            async with searcher:
                results = await searcher.search_repositories("test", limit=1)
                
                assert len(results) == 1
                assert results[0].name == 'test-repo'
                assert results[0].full_name == 'test-owner/test-repo'
                assert results[0].stars == 100
                assert results[0].language == 'Python'
    
    @pytest.mark.asyncio
    async def test_get_readme_content_success(self, searcher):
        """Test successful README content retrieval"""
        mock_response_data = {
            'content': 'SGVsbG8gV29ybGQ=',  # Base64 encoded "Hello World"
            'encoding': 'base64'
        }
        
        with patch.object(searcher, 'session') as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value=mock_response_data)
            mock_session.get.return_value.__aenter__.return_value = mock_response
            
            async with searcher:
                content = await searcher.get_readme_content("test-owner", "test-repo")
                assert content == "Hello World"
    
    @pytest.mark.asyncio
    async def test_get_readme_content_not_found(self, searcher):
        """Test README content retrieval when not found"""
        with patch.object(searcher, 'session') as mock_session:
            mock_response = AsyncMock()
            mock_response.status = 404
            mock_session.get.return_value.__aenter__.return_value = mock_response
            
            async with searcher:
                content = await searcher.get_readme_content("test-owner", "test-repo")
                assert content is None


if __name__ == "__main__":
    pytest.main([__file__]) 