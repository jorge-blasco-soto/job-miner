"""Scraper package initialization."""
from jobminer.scrapers.base import BaseScraper
from jobminer.scrapers.job_boards import get_all_scrapers

__all__ = ['BaseScraper', 'get_all_scrapers']
