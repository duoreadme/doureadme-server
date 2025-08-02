#!/usr/bin/env python3
"""
GitHub README Searcher - Usage Examples (Direct API Version)

This script demonstrates how to use the GitHub README Searcher with direct API calls.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def example_direct_api():
    """Example using the direct API version"""
    print("=== Direct API Version Example ===")
    
    try:
        from github_api_searcher import GitHubAPISearcher
        
        github_token = os.getenv('GITHUB_TOKEN')
        if not github_token:
            print("GITHUB_TOKEN not set, skipping direct API example")
            return
        
        # Use async context manager
        async with GitHubAPISearcher(github_token) as searcher:
            # Search for Python repositories
            print("Searching for Python repositories...")
            repositories = await searcher.search_and_get_readmes(
                domain="python",
                limit=2
            )
            
            print(f"Found {len(repositories)} repositories:")
            for i, repo in enumerate(repositories, 1):
                print(f"\n{i}. {repo.full_name}")
                print(f"   Stars: {repo.stars:,}")
                print(f"   Language: {repo.language}")
                print(f"   Description: {repo.description}")
                
                if repo.readme_content:
                    preview = repo.readme_content[:200].replace('\n', ' ')
                    print(f"   README Preview: {preview}...")
                else:
                    print("   README: Not available")
                    
    except ImportError:
        print("Direct API version not available")
    except Exception as e:
        print(f"Error in direct API example: {e}")

def example_cli_commands():
    """Show example CLI commands"""
    print("\n=== CLI Usage Examples ===")
    
    print("Direct API version:")
    print("  python cli_api.py 'machine learning' --limit 5")
    print("  python cli_api.py 'react' --limit 3 --no-readme")
    print("  python cli_api.py 'python' --limit 10 --output results.json")

def example_api_endpoints():
    """Show example API endpoints"""
    print("\n=== API Endpoints Examples ===")
    
    print("API Server (port 5088):")
    print("  Start server: python api_server_direct.py")
    print("  Or use: ./start.sh api")
    print()
    print("Available endpoints:")
    print("  GET  http://localhost:5088/                    # Root endpoint")
    print("  GET  http://localhost:5088/health              # Health check")
    print("  GET  http://localhost:5088/docs                # API documentation")
    print("  POST http://localhost:5088/search              # Search with README")
    print("  GET  http://localhost:5088/search/{domain}     # Simple search")
    print("  GET  http://localhost:5088/search/{domain}/no-readme  # Fast search")
    print("  GET  http://localhost:5088/domains             # Popular domains")
    print("  GET  http://localhost:5088/stats               # API statistics")
    print()
    print("Example API calls:")
    print("  curl -X POST http://localhost:5088/search \\")
    print("    -H 'Content-Type: application/json' \\")
    print("    -d '{\"domain\": \"machine learning\", \"limit\": 5}'")
    print()
    print("  curl 'http://localhost:5088/search/machine%20learning?limit=5'")
    print()
    print("  curl 'http://localhost:5088/search/machine%20learning/no-readme?limit=5'")

async def main():
    """Main function"""
    print("GitHub README Searcher - Usage Examples (Direct API Version)")
    print("=" * 60)
    
    # Check if GitHub token is available
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("⚠️  GITHUB_TOKEN not set!")
        print("To run the examples, set your GitHub token:")
        print("  export GITHUB_TOKEN=your_github_token")
        print("  or create a .env file with: GITHUB_TOKEN=your_github_token")
        print()
    
    # Run examples
    await example_direct_api()
    example_cli_commands()
    example_api_endpoints()
    
    print("\n" + "=" * 60)
    print("For more information, see README.md")

if __name__ == "__main__":
    asyncio.run(main()) 