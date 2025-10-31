FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Set working directory
WORKDIR /app

# Install Poetry
RUN pip install poetry==1.7.0

# Copy dependency files
COPY pyproject.toml poetry.lock* ./

# Install dependencies
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# Copy application code
COPY jobminer ./jobminer
COPY .env.example .env

# Create data directory
RUN mkdir -p /app/data

# Expose port for Ollama (optional, for debugging)
EXPOSE 11434

# Set entrypoint
ENTRYPOINT ["python", "-m", "jobminer.main"]
