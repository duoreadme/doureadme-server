#!/usr/bin/env python3
"""
Test example for GitHub README Searcher - Direct API Version

This script demonstrates how to use the GitHub README Searcher
without requiring a GitHub token (for testing purposes).
"""

import asyncio
import json
from typing import List
from dataclasses import dataclass

@dataclass
class MockRepositoryInfo:
    """Mock repository information for testing"""
    name: str
    full_name: str
    description: str
    stars: int
    language: str
    url: str
    readme_content: str = None

class MockGitHubAPISearcher:
    """Mock GitHub API Searcher for testing without GitHub token"""
    
    def __init__(self, github_token: str = "mock_token"):
        self.github_token = github_token
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        print("Mock: Connected to GitHub API")
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        print("Mock: Disconnected from GitHub API")
    
    async def search_and_get_readmes(self, domain: str, limit: int = 5) -> List[MockRepositoryInfo]:
        """Mock search with sample data"""
        print(f"Mock: Searching for '{domain}' repositories (top {limit} by stars)...")
        
        # Sample repositories for different domains
        sample_repos = {
            "machine learning": [
                MockRepositoryInfo(
                    name="tensorflow",
                    full_name="tensorflow/tensorflow",
                    description="An Open Source Machine Learning Framework for Everyone",
                    stars=175000,
                    language="Python",
                    url="https://github.com/tensorflow/tensorflow",
                    readme_content="# TensorFlow\n\nTensorFlow is an open source software library for numerical computation using data flow graphs."
                ),
                MockRepositoryInfo(
                    name="pytorch",
                    full_name="pytorch/pytorch",
                    description="Tensors and Dynamic neural networks in Python with strong GPU acceleration",
                    stars=68000,
                    language="Python",
                    url="https://github.com/pytorch/pytorch",
                    readme_content="# PyTorch\n\nPyTorch is a machine learning framework that accelerates the path from research prototyping to production deployment."
                )
            ],
            "web development": [
                MockRepositoryInfo(
                    name="react",
                    full_name="facebook/react",
                    description="The library for web and native user interfaces",
                    stars=200000,
                    language="JavaScript",
                    url="https://github.com/facebook/react",
                    readme_content="# React\n\nReact is a JavaScript library for building user interfaces."
                ),
                MockRepositoryInfo(
                    name="vue",
                    full_name="vuejs/vue",
                    description="Vue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web.",
                    stars=200000,
                    language="JavaScript",
                    url="https://github.com/vuejs/vue",
                    readme_content="# Vue.js\n\nVue.js is a progressive, incrementally-adoptable JavaScript framework for building UI on the web."
                )
            ],
            "python": [
                MockRepositoryInfo(
                    name="requests",
                    full_name="psf/requests",
                    description="A simple, yet elegant HTTP library.",
                    stars=49000,
                    language="Python",
                    url="https://github.com/psf/requests",
                    readme_content="# Requests\n\nRequests is an elegant and simple HTTP library for Python, built for human beings."
                )
            ]
        }
        
        # Return sample data for the requested domain
        repos = sample_repos.get(domain.lower(), [])
        return repos[:limit]

async def test_search():
    """Test the search functionality with mock data"""
    print("=== GitHub README Searcher Test (Direct API Version) ===\n")
    
    # Create mock searcher
    async with MockGitHubAPISearcher() as searcher:
        # Test different domains
        test_domains = ["machine learning", "web development", "python"]
        
        for domain in test_domains:
            print(f"\n--- Testing domain: '{domain}' ---")
            
            # Search repositories
            repositories = await searcher.search_and_get_readmes(
                domain=domain,
                limit=2
            )
            
            # Display results
            print(f"Found {len(repositories)} repositories:")
            for i, repo in enumerate(repositories, 1):
                print(f"\n{i}. {repo.full_name}")
                print(f"   Stars: {repo.stars:,}")
                print(f"   Language: {repo.language}")
                print(f"   Description: {repo.description}")
                print(f"   URL: {repo.url}")
                
                if repo.readme_content:
                    preview = repo.readme_content[:100].replace('\n', ' ')
                    if len(repo.readme_content) > 100:
                        preview += "..."
                    print(f"   README Preview: {preview}")
                else:
                    print("   README: Not available")
        
        print(f"\n=== Test completed successfully! ===")

def test_cli_parsing():
    """Test CLI argument parsing"""
    print("\n=== Testing CLI Argument Parsing ===")
    
    # Simulate CLI arguments
    test_args = [
        ["machine learning", "--limit", "5"],
        ["react", "--limit", "3", "--no-readme"],
        ["python", "--limit", "10", "--output", "results.json"],
        ["blockchain", "--limit", "3", "--format", "txt", "--output", "results.txt"]
    ]
    
    for i, args in enumerate(test_args, 1):
        print(f"\nTest {i}: {' '.join(args)}")
        print(f"  Domain: {args[0]}")
        
        # Parse arguments manually for demonstration
        limit = 5
        no_readme = False
        output = None
        format_type = "json"
        
        for j, arg in enumerate(args[1:], 1):
            if arg == "--limit" and j + 1 < len(args):
                limit = int(args[j + 1])
            elif arg == "--no-readme":
                no_readme = True
            elif arg == "--output" and j + 1 < len(args):
                output = args[j + 1]
            elif arg == "--format" and j + 1 < len(args):
                format_type = args[j + 1]
        
        print(f"  Limit: {limit}")
        print(f"  No README: {no_readme}")
        print(f"  Output: {output}")
        print(f"  Format: {format_type}")

def test_api_endpoints():
    """Test API endpoint examples"""
    print("\n=== Testing API Endpoints ===")
    
    # Example API requests
    api_examples = [
        {
            "method": "GET",
            "endpoint": "/health",
            "description": "Health check"
        },
        {
            "method": "POST",
            "endpoint": "/search",
            "body": {
                "domain": "machine learning",
                "limit": 5
            },
            "description": "Search repositories with README"
        },
        {
            "method": "GET",
            "endpoint": "/search/machine%20learning?limit=5",
            "description": "Simple search with README"
        },
        {
            "method": "GET",
            "endpoint": "/search/machine%20learning/no-readme?limit=5",
            "description": "Fast search without README"
        },
        {
            "method": "GET",
            "endpoint": "/domains",
            "description": "Get popular domains"
        },
        {
            "method": "GET",
            "endpoint": "/stats",
            "description": "Get API statistics"
        }
    ]
    
    for example in api_examples:
        print(f"\n{example['method']} {example['endpoint']}")
        print(f"  Description: {example['description']}")
        if 'body' in example:
            print(f"  Body: {json.dumps(example['body'], indent=2)}")

if __name__ == "__main__":
    # Run tests
    asyncio.run(test_search())
    test_cli_parsing()
    test_api_endpoints()
    
    print("\n=== All tests completed! ===")
    print("\nTo run the actual service:")
    print("1. Set your GitHub token: export GITHUB_TOKEN=your_token")
    print("2. Run CLI: python cli_api.py 'machine learning' --limit 5")
    print("3. Run API: python api_server_direct.py")
    print("4. Or use: ./start.sh api") 