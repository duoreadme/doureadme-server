.PHONY: help install install-dev test lint format clean run-api docker-build docker-run

help: ## Show this help message
	@echo "GitHub README Searcher - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install production dependencies
	pip install -r requirements.txt

install-dev: ## Install development dependencies
	pip install -r requirements.txt
	pip install -e ".[dev]"

test: ## Run tests
	pytest tests/ -v

test-coverage: ## Run tests with coverage
	pytest tests/ --cov=app --cov-report=html --cov-report=term

lint: ## Run linting
	flake8 app/ tests/
	mypy app/

format: ## Format code with black
	black app/ tests/

format-check: ## Check code formatting
	black --check app/ tests/

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/ dist/ .pytest_cache/ .coverage htmlcov/

run-api: ## Start the API server
	python main.py

docker-build: ## Build Docker image
	docker build -t github-readme-searcher .

docker-run: ## Run Docker container
	docker run -p 5088:5088 --env-file .env github-readme-searcher

check: format-check lint test ## Run all checks (format, lint, test)

dev: install-dev ## Install dev dependencies and run all checks
	$(MAKE) check 