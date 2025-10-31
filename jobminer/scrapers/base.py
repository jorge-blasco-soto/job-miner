"""Base scraper class and utilities."""
import logging
from abc import ABC, abstractmethod
from typing import List

from jobminer.models import Job

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for job scrapers."""

    def __init__(self, name: str):
        self.name = name
        self.jobs: List[Job] = []

    @abstractmethod
    def scrape(self, keywords: List[str], max_jobs: int = 50) -> List[Job]:
        """
        Scrape jobs from the source.

        Args:
            keywords: List of job title keywords to search for
            max_jobs: Maximum number of jobs to scrape

        Returns:
            List of Job objects
        """
        pass

    def filter_remote(self, jobs: List[Job]) -> List[Job]:
        """Filter for remote jobs only."""
        return [job for job in jobs if job.is_remote]

    def filter_by_company(self, jobs: List[Job], company_names: List[str]) -> List[Job]:
        """Filter jobs from specific companies."""
        company_names_lower = [name.lower() for name in company_names]
        filtered = []
        for job in jobs:
            if any(company.lower() in job.company.lower() for company in company_names_lower):
                filtered.append(job)
        return filtered

    def deduplicate(self, jobs: List[Job]) -> List[Job]:
        """Remove duplicate jobs based on URL."""
        seen_urls = set()
        unique_jobs = []
        for job in jobs:
            url_str = str(job.url)
            if url_str not in seen_urls:
                seen_urls.add(url_str)
                unique_jobs.append(job)
        return unique_jobs
