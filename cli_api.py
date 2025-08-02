#!/usr/bin/env python3
"""
Command Line Interface for GitHub README Searcher - Direct API Version

This script provides a command-line interface to search GitHub repositories
and retrieve README content using direct GitHub API calls.
"""

import asyncio
import argparse
import json
import os
import sys
from typing import Optional
from dotenv import load_dotenv

from github_api_searcher import GitHubAPISearcher

def save_results_to_file(repositories, output_file: str, format_type: str = 'json'):
    """Save search results to a file"""
    try:
        if format_type == 'json':
            # Convert repositories to JSON-serializable format
            data = []
            for repo in repositories:
                repo_data = {
                    'name': repo.name,
                    'full_name': repo.full_name,
                    'description': repo.description,
                    'stars': repo.stars,
                    'language': repo.language,
                    'url': repo.url,
                    'readme_content': repo.readme_content
                }
                data.append(repo_data)
            
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                
        elif format_type == 'txt':
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"GitHub README Search Results\n")
                f.write(f"{'='*50}\n\n")
                
                for i, repo in enumerate(repositories, 1):
                    f.write(f"{i}. {repo.full_name}\n")
                    f.write(f"   Stars: {repo.stars:,}\n")
                    f.write(f"   Language: {repo.language}\n")
                    f.write(f"   Description: {repo.description}\n")
                    f.write(f"   URL: {repo.url}\n")
                    
                    if repo.readme_content:
                        f.write(f"   README Content:\n")
                        f.write(f"   {'-'*30}\n")
                        f.write(repo.readme_content)
                        f.write(f"\n   {'-'*30}\n")
                    else:
                        f.write(f"   README: Not available\n")
                    
                    f.write(f"\n")
        
        print(f"Results saved to {output_file}")
        
    except Exception as e:
        print(f"Error saving results to file: {e}")

def display_results(repositories, max_readme_length: int = 500, quiet: bool = False):
    """Display search results"""
    if quiet:
        # Quiet mode - just show basic info
        for repo in repositories:
            print(f"{repo.full_name} ({repo.stars:,} stars)")
        return
    
    print(f"\nFound {len(repositories)} repositories:")
    print(f"{'='*60}")
    
    for i, repo in enumerate(repositories, 1):
        print(f"\n{i}. {repo.full_name}")
        print(f"   Stars: {repo.stars:,}")
        print(f"   Language: {repo.language}")
        print(f"   Description: {repo.description}")
        print(f"   URL: {repo.url}")
        
        if repo.readme_content:
            # Truncate README content if too long
            if len(repo.readme_content) > max_readme_length:
                preview = repo.readme_content[:max_readme_length].replace('\n', ' ')
                preview += "..."
                print(f"   README Preview: {preview}")
            else:
                print(f"   README Content:")
                print(f"   {'-'*40}")
                print(repo.readme_content)
                print(f"   {'-'*40}")
        else:
            print("   README: Not available")
        
        print()

async def main():
    """Main function"""
    # Load environment variables
    load_dotenv()
    
    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Search GitHub repositories and retrieve README content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "machine learning" --limit 5
  %(prog)s "react" --limit 3 --no-readme
  %(prog)s "python" --limit 10 --output results.json
  %(prog)s "blockchain" --limit 3 --format txt --output results.txt
  %(prog)s "web development" --limit 5 --max-readme-length 1000
        """
    )
    
    parser.add_argument(
        'domain',
        help='Domain/topic to search for (e.g., "machine learning", "web development")'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        default=5,
        help='Maximum number of repositories to return (default: 5)'
    )
    
    parser.add_argument(
        '--no-readme',
        action='store_true',
        help='Skip retrieving README content (faster)'
    )
    
    parser.add_argument(
        '--output',
        help='Save results to file'
    )
    
    parser.add_argument(
        '--format',
        choices=['json', 'txt'],
        default='json',
        help='Output format for file (default: json)'
    )
    
    parser.add_argument(
        '--max-readme-length',
        type=int,
        default=500,
        help='Maximum README content length to display (default: 500)'
    )
    
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Quiet mode - minimal output'
    )
    
    args = parser.parse_args()
    
    # Check for GitHub token
    github_token = os.getenv('GITHUB_TOKEN')
    if not github_token:
        print("Error: GITHUB_TOKEN environment variable is not set")
        print("Please set it with: export GITHUB_TOKEN=your_github_token")
        print("Or create a .env file with: GITHUB_TOKEN=your_github_token")
        sys.exit(1)
    
    try:
        # Use async context manager
        async with GitHubAPISearcher(github_token) as searcher:
            print(f"Searching for '{args.domain}' repositories...")
            print(f"Sorting by stars (descending) and returning top {args.limit} repositories")
            
            if args.no_readme:
                # Search repositories only (no README)
                repositories = await searcher.search_repositories(
                    domain=args.domain,
                    limit=args.limit
                )
            else:
                # Search repositories and get README content
                repositories = await searcher.search_and_get_readmes(
                    domain=args.domain,
                    limit=args.limit
                )
            
            # Display results
            display_results(repositories, args.max_readme_length, args.quiet)
            
            # Save to file if requested
            if args.output:
                save_results_to_file(repositories, args.output, args.format)
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main()) 