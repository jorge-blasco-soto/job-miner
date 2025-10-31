.PHONY: help install setup run test clean docker-build docker-run lint format

help:  ## Show this help message
	@echo "JobMiner - Automated Job Scraper"
	@echo ""
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install dependencies with Poetry
	poetry install

setup:  ## Initial setup (install deps, setup Ollama)
	@echo "Installing dependencies..."
	poetry install
	@echo ""
	@echo "Setting up environment..."
	cp -n .env.example .env || true
	mkdir -p data
	@echo ""
	@echo "Checking Ollama installation..."
	@if command -v ollama >/dev/null 2>&1; then \
		echo "✅ Ollama is installed"; \
		echo "Pulling llama2 model..."; \
		ollama pull llama2; \
	else \
		echo "⚠️  Ollama not installed. Install from: https://ollama.com"; \
		echo "Or run: curl -fsSL https://ollama.com/install.sh | sh"; \
	fi
	@echo ""
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Next steps:"
	@echo "  1. Start Ollama: ollama serve"
	@echo "  2. Run scraper: make run"

run:  ## Run the job scraper
	@echo "Starting job scraper..."
	poetry run jobminer

run-docker:  ## Run with Docker Compose
	docker-compose up

docker-build:  ## Build Docker image
	docker build -t jobminer:latest .

test:  ## Run tests (when implemented)
	poetry run pytest

lint:  ## Run linting
	poetry run flake8 jobminer
	poetry run mypy jobminer

format:  ## Format code with Black
	poetry run black jobminer

clean:  ## Clean up generated files
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -f jobminer.log
	@echo "Cleaned up temporary files"

clean-data:  ## Clean up scraped data (keeps sample)
	@read -p "Are you sure you want to delete all scraped data? [y/N] " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		rm -f data/jobs_*.json data/jobs_*.csv data/result_*.json; \
		echo "Data cleaned (sample_jobs.json preserved)"; \
	else \
		echo "Cancelled"; \
	fi

check-ollama:  ## Check if Ollama is running
	@echo "Checking Ollama status..."
	@if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then \
		echo "✅ Ollama is running"; \
		curl -s http://localhost:11434/api/tags | python3 -m json.tool; \
	else \
		echo "❌ Ollama is not running"; \
		echo "Start it with: ollama serve"; \
		exit 1; \
	fi

view-latest:  ## View latest job results
	@if [ -f data/jobs_latest.json ]; then \
		echo "Latest job results:"; \
		echo ""; \
		python3 -c "import json; jobs = json.load(open('data/jobs_latest.json')); print(f'Total jobs: {len(jobs)}'); [print(f\"  {i+1}. [{job.get('relevance_score', 'N/A'):.2f}] {job['company']} - {job['title']}\") for i, job in enumerate(sorted(jobs, key=lambda x: x.get('relevance_score', 0), reverse=True)[:20])]"; \
	else \
		echo "No results yet. Run 'make run' first."; \
	fi

init-git:  ## Initialize git repository
	@if [ ! -d .git ]; then \
		git init; \
		git add .; \
		git commit -m "Initial commit: JobMiner setup"; \
		echo ""; \
		echo "✅ Git repository initialized"; \
		echo ""; \
		echo "Next steps:"; \
		echo "  1. Create a GitHub repository"; \
		echo "  2. git remote add origin <your-repo-url>"; \
		echo "  3. git push -u origin main"; \
	else \
		echo "Git repository already initialized"; \
	fi
