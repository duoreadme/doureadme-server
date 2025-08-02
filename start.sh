#!/bin/bash

# GitHub README Searcher Startup Script - Direct API Version

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to check environment
check_environment() {
    print_status "Checking environment..."
    
    # Check Python
    if ! command_exists python; then
        print_error "Python is not installed. Please install Python 3.8+"
        exit 1
    fi
    
    # Check Python version
    python_version=$(python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
    print_status "Python version: $python_version"
    
    print_success "Environment check passed"
}

# Function to check GitHub token
check_github_token() {
    if [ -z "$GITHUB_TOKEN" ]; then
        if [ -f ".env" ]; then
            export $(cat .env | grep -v '^#' | xargs)
        fi
        
        if [ -z "$GITHUB_TOKEN" ]; then
            print_error "GITHUB_TOKEN environment variable is not set"
            print_status "Please set your GitHub token:"
            print_status "1. Create a .env file: cp env.example .env"
            print_status "2. Edit .env file and add your GitHub token"
            print_status "3. Or set environment variable: export GITHUB_TOKEN=your_token"
            exit 1
        fi
    fi
    
    print_success "GitHub token found"
}

# Function to install dependencies
install_dependencies() {
    print_status "Installing Python dependencies..."
    
    if [ ! -f "requirements.txt" ]; then
        print_error "requirements.txt not found"
        exit 1
    fi
    
    pip install -r requirements.txt
    print_success "Dependencies installed"
}

# Function to start API server
start_api_server() {
    print_status "Starting API server on port 5088..."
    print_status "Server will be available at: http://localhost:5088"
    print_status "API documentation: http://localhost:5088/docs"
    print_status "Health check: http://localhost:5088/health"
    print_status "Press Ctrl+C to stop the server"
    
    python api_server_direct.py
}

# Function to run CLI
run_cli() {
    local domain="$1"
    local limit="${2:-5}"
    
    print_status "Running CLI search..."
    print_status "Domain: $domain"
    print_status "Limit: $limit"
    
    python cli_api.py "$domain" --limit "$limit"
}

# Function to show help
show_help() {
    echo "GitHub README Searcher - Direct API Version"
    echo ""
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  api                    Start the API server on port 5088"
    echo "  cli <domain> [limit]   Run CLI search"
    echo "  test                   Run test example"
    echo "  install                Install dependencies"
    echo "  check                  Check environment"
    echo "  help                   Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 api                                    # Start API server"
    echo "  $0 cli 'machine learning' 5              # Search ML repos"
    echo "  $0 cli 'react' 3                         # Search React repos"
    echo "  $0 test                                  # Run test example"
    echo ""
    echo "Environment:"
    echo "  GITHUB_TOKEN            GitHub Personal Access Token (required)"
    echo "  GITHUB_HOST             GitHub API host (optional, default: https://api.github.com)"
    echo ""
    echo "API Endpoints:"
    echo "  http://localhost:5088/                   # Root endpoint"
    echo "  http://localhost:5088/docs               # API documentation"
    echo "  http://localhost:5088/health             # Health check"
    echo "  http://localhost:5088/search             # Search repositories"
    echo "  http://localhost:5088/domains            # Popular domains"
    echo ""
    echo "Features:"
    echo "  - Sort by stars (descending)"
    echo "  - No minimum stars requirement"
    echo "  - Direct GitHub API integration"
    echo "  - No Docker required"
}

# Main script
main() {
    case "${1:-help}" in
        "api")
            check_environment
            check_github_token
            install_dependencies
            start_api_server
            ;;
        "cli")
            if [ -z "$2" ]; then
                print_error "Domain is required for CLI mode"
                echo "Usage: $0 cli <domain> [limit]"
                exit 1
            fi
            check_environment
            check_github_token
            install_dependencies
            run_cli "$2" "$3"
            ;;
        "test")
            print_status "Running test example..."
            python test_example.py
            ;;
        "install")
            check_environment
            install_dependencies
            ;;
        "check")
            check_environment
            check_github_token
            print_success "All checks passed!"
            ;;
        "help"|*)
            show_help
            ;;
    esac
}

# Run main function with all arguments
main "$@" 