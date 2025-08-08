# GitHub README Searcher API Documentation

## Overview

The GitHub README Searcher API provides endpoints for searching GitHub repositories and retrieving README content. The API is built with FastAPI and provides both REST endpoints and interactive documentation.

## Base URL

```
http://localhost:5088/api/v1
```

## Authentication

Currently, the API uses GitHub Personal Access Token for authentication. Set the `GITHUB_TOKEN` environment variable with your GitHub token.

## Endpoints

### Health Check

**GET** `/health`

Check the health status of the API and GitHub connection.

**Response:**
```json
{
  "status": "healthy",
  "api_connected": true,
  "github_token_configured": true
}
```

### Search Repositories (POST)

**POST** `/search`

Search for repositories with README content using JSON request body.

**Request Body:**
```json
{
  "domain": "machine learning",
  "limit": 5
}
```

**Response:**
```json
{
  "domain": "machine learning",
  "repositories": [
    {
      "name": "tensorflow",
      "full_name": "tensorflow/tensorflow",
      "description": "An Open Source Machine Learning Framework for Everyone",
      "stars": 175000,
      "language": "C++",
      "url": "https://github.com/tensorflow/tensorflow",
      "readme_content": "# TensorFlow\n\nAn Open Source Machine Learning Framework..."
    }
  ],
  "total_count": 1
}
```

### Search Repositories (GET with Query)

**GET** `/search?keywords=machine%20learning&limit=5`

Search for repositories using query parameters.

**Parameters:**
- `keywords` (required): Search keywords
- `limit` (optional): Maximum number of repositories (default: 5, max: 100)

### Search Repositories (GET with Path)

**GET** `/search/{domain}?limit=5`

Search for repositories using path parameter.

**Parameters:**
- `domain` (path): Search domain
- `limit` (query, optional): Maximum number of repositories (default: 5, max: 100)

### Search Repositories (No README)

**GET** `/search/{domain}/no-readme?limit=5`

Search for repositories without retrieving README content (faster).

**Parameters:**
- `domain` (path): Search domain
- `limit` (query, optional): Maximum number of repositories (default: 5, max: 100)

### Get Popular Domains

**GET** `/domains`

Get a list of popular search domains.

**Response:**
```json
{
  "popular_domains": [
    "machine learning",
    "artificial intelligence",
    "web development",
    "python",
    "javascript"
  ],
  "total_count": 27,
  "description": "Popular technology domains for GitHub repository search"
}
```

### Get API Statistics

**GET** `/stats`

Get API usage statistics.

**Response:**
```json
{
  "total_searches": 42,
  "total_repositories_found": 210,
  "average_repositories_per_search": 5.0,
  "most_searched_domains": [
    "machine learning",
    "python",
    "react"
  ]
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Validation error"
}
```

### 500 Internal Server Error
```json
{
  "detail": "Search failed: GitHub API error"
}
```

## Rate Limiting

The API respects GitHub's rate limiting. When rate limits are exceeded, the API will return appropriate error responses.

## Interactive Documentation

Visit `http://localhost:5088/docs` for interactive API documentation (Swagger UI) or `http://localhost:5088/redoc` for ReDoc documentation.

## Examples

### Using curl

```bash
# Health check
curl http://localhost:5088/api/v1/health

# Search repositories
curl -X POST http://localhost:5088/api/v1/search \
  -H "Content-Type: application/json" \
  -d '{"domain": "python", "limit": 3}'

# Simple search
curl "http://localhost:5088/api/v1/search/python?limit=3"

# Get popular domains
curl http://localhost:5088/api/v1/domains
```

### Using Python requests

```python
import requests

# Search repositories
response = requests.post(
    "http://localhost:5088/api/v1/search",
    json={"domain": "machine learning", "limit": 5}
)
repositories = response.json()

# Get statistics
stats = requests.get("http://localhost:5088/api/v1/stats").json()
print(f"Total searches: {stats['total_searches']}")
``` 