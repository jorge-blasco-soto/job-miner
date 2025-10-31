"""Configuration settings for the job scraper."""
from pathlib import Path
from typing import List

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM Configuration
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "llama2"
    openai_api_key: str | None = None
    openai_base_url: str | None = None
    openai_model: str = "gpt-3.5-turbo"

    # Groq Configuration (free tier, OpenAI-compatible)
    groq_api_key: str | None = None
    groq_model: str = "llama-3.1-8b-instant"  # Fast and free

    # Job Search Configuration
    target_roles: str = "data engineer,senior data engineer,software engineer,solutions architect"
    min_employees: int = 200
    min_years_in_business: int = 5
    remote_only: bool = True
    prefer_public_companies: bool = True

    # Scraper Configuration
    max_jobs_per_run: int = 100
    headless_browser: bool = True

    # Data Storage
    data_dir: Path = Path("./data")
    output_format: str = "json,csv"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def target_roles_list(self) -> List[str]:
        """Parse target roles into a list."""
        return [role.strip() for role in self.target_roles.split(",")]

    @property
    def output_formats(self) -> List[str]:
        """Parse output formats into a list."""
        return [fmt.strip() for fmt in self.output_format.split(",")]


settings = Settings()
