"""Scraper for public job boards using APIs and web scraping."""
import logging
import time
from typing import List
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup

from jobminer.companies import (get_company_info, get_company_names,
                                is_established_company)
from jobminer.config import settings
from jobminer.models import Job
from jobminer.scrapers.base import BaseScraper

logger = logging.getLogger(__name__)


class RemoteOKScraper(BaseScraper):
    """Scraper for RemoteOK (free, no API key needed)."""

    def __init__(self):
        super().__init__("RemoteOK")
        self.base_url = "https://remoteok.com/api"

    def scrape(self, keywords: List[str], max_jobs: int = 50) -> List[Job]:
        """Scrape jobs from RemoteOK API."""
        jobs = []

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(self.base_url, headers=headers, timeout=10)
            response.raise_for_status()

            data = response.json()
            # First item is metadata, skip it
            job_listings = data[1:] if len(data) > 1 else []

            company_names = get_company_names()

            for listing in job_listings[:max_jobs * 3]:  # Get extra to filter
                try:
                    company = listing.get('company', '')
                    position = listing.get('position', '')

                    # Check if it's an established company
                    if not is_established_company(company):
                        continue

                    # Check if position matches keywords
                    position_lower = position.lower()
                    if not any(keyword.lower() in position_lower for keyword in keywords):
                        continue

                    job = Job(
                        title=position,
                        company=company,
                        company_info=get_company_info(company),
                        url=f"https://remoteok.com/remote-jobs/{listing.get('id', '')}",
                        location=listing.get('location', 'Remote'),
                        is_remote=True,
                        description=listing.get('description', ''),
                        posted_date=None,
                        salary_range=listing.get('salary_min', '')
                    )
                    jobs.append(job)

                    if len(jobs) >= max_jobs:
                        break

                except Exception as e:
                    logger.error(f"Error parsing RemoteOK job: {e}")
                    continue

            logger.info(f"RemoteOK: Scraped {len(jobs)} jobs")

        except Exception as e:
            logger.error(f"Error scraping RemoteOK: {e}")

        return jobs


class WWRScraper(BaseScraper):
    """Scraper for We Work Remotely (web scraping)."""

    def __init__(self):
        super().__init__("WeWorkRemotely")
        self.base_url = "https://weworkremotely.com"

    def scrape(self, keywords: List[str], max_jobs: int = 50) -> List[Job]:
        """Scrape jobs from We Work Remotely."""
        jobs = []

        try:
            # Search in programming category
            url = f"{self.base_url}/categories/remote-programming-jobs"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            listings = soup.find_all('li', class_='feature')

            company_names = get_company_names()

            for listing in listings[:max_jobs * 2]:
                try:
                    title_elem = listing.find('span', class_='title')
                    company_elem = listing.find('span', class_='company')
                    link_elem = listing.find('a')

                    if not all([title_elem, company_elem, link_elem]):
                        continue

                    title = title_elem.text.strip()
                    company = company_elem.text.strip()
                    job_url = self.base_url + link_elem['href']

                    # Check if it's an established company
                    if not is_established_company(company):
                        continue

                    # Check if position matches keywords
                    title_lower = title.lower()
                    if not any(keyword.lower() in title_lower for keyword in keywords):
                        continue

                    job = Job(
                        title=title,
                        company=company,
                        company_info=get_company_info(company),
                        url=job_url,
                        location="Remote",
                        is_remote=True,
                        description=None
                    )
                    jobs.append(job)

                    if len(jobs) >= max_jobs:
                        break

                except Exception as e:
                    logger.error(f"Error parsing WWR job: {e}")
                    continue

            logger.info(f"WWR: Scraped {len(jobs)} jobs")

        except Exception as e:
            logger.error(f"Error scraping WWR: {e}")

        return jobs


class RemotiveScraper(BaseScraper):
    """Scraper for Remotive (web scraping)."""

    def __init__(self):
        super().__init__("Remotive")
        self.base_url = "https://remotive.com"

    def scrape(self, keywords: List[str], max_jobs: int = 50) -> List[Job]:
        """Scrape jobs from Remotive."""
        jobs = []

        try:
            url = f"{self.base_url}/remote-jobs/software-dev"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
            }

            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            listings = soup.find_all('li', class_='job-tile')

            company_names = get_company_names()

            for listing in listings[:max_jobs * 2]:
                try:
                    title_elem = listing.find('a', class_='job-tile-title')
                    company_elem = listing.find('span', class_='company')

                    if not all([title_elem, company_elem]):
                        continue

                    title = title_elem.text.strip()
                    company = company_elem.text.strip()
                    job_url = title_elem['href']
                    if not job_url.startswith('http'):
                        job_url = self.base_url + job_url

                    # Check if it's an established company
                    if not is_established_company(company):
                        continue

                    # Check if position matches keywords
                    title_lower = title.lower()
                    if not any(keyword.lower() in title_lower for keyword in keywords):
                        continue

                    job = Job(
                        title=title,
                        company=company,
                        company_info=get_company_info(company),
                        url=job_url,
                        location="Remote",
                        is_remote=True,
                        description=None
                    )
                    jobs.append(job)

                    if len(jobs) >= max_jobs:
                        break

                except Exception as e:
                    logger.error(f"Error parsing Remotive job: {e}")
                    continue

            logger.info(f"Remotive: Scraped {len(jobs)} jobs")

        except Exception as e:
            logger.error(f"Error scraping Remotive: {e}")

        return jobs


class CompanyCareersPageScraper(BaseScraper):
    """Scraper for direct company career pages (Greenhouse, Lever, etc.)."""

    def __init__(self):
        super().__init__("CompanyCareersPage")
        self.greenhouse_companies = [
            "Databricks", "Snowflake", "GitLab", "Stripe", "Coinbase",
            "Spotify", "Airbnb", "DoorDash", "Robinhood"
        ]
        self.lever_companies = [
            "Netflix", "Canva", "Figma", "Discord", "Notion"
        ]

    def scrape(self, keywords: List[str], max_jobs: int = 50) -> List[Job]:
        """Scrape jobs from company career pages."""
        jobs = []

        # Scrape Greenhouse boards
        for company in self.greenhouse_companies[:10]:
            if len(jobs) >= max_jobs:
                break

            try:
                jobs.extend(self._scrape_greenhouse(company, keywords, max_jobs // 10))
                time.sleep(1)  # Be respectful
            except Exception as e:
                logger.error(f"Error scraping {company} Greenhouse: {e}")

        # Scrape Lever boards
        for company in self.lever_companies[:10]:
            if len(jobs) >= max_jobs:
                break

            try:
                jobs.extend(self._scrape_lever(company, keywords, max_jobs // 10))
                time.sleep(1)
            except Exception as e:
                logger.error(f"Error scraping {company} Lever: {e}")

        logger.info(f"CompanyCareersPage: Scraped {len(jobs)} jobs")
        return jobs[:max_jobs]

    def _scrape_greenhouse(self, company: str, keywords: List[str], max_jobs: int) -> List[Job]:
        """Scrape a Greenhouse job board."""
        jobs = []
        company_slug = company.lower().replace(' ', '-')
        url = f"https://boards.greenhouse.io/{company_slug}"

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            listings = soup.find_all('div', class_='opening')

            for listing in listings[:max_jobs]:
                try:
                    title_elem = listing.find('a')
                    location_elem = listing.find('span', class_='location')

                    if not title_elem:
                        continue

                    title = title_elem.text.strip()
                    location = location_elem.text.strip() if location_elem else "Unknown"
                    job_url = title_elem['href']
                    if not job_url.startswith('http'):
                        job_url = f"https://boards.greenhouse.io{job_url}"

                    # Check keywords
                    title_lower = title.lower()
                    if not any(keyword.lower() in title_lower for keyword in keywords):
                        continue

                    # Check if remote
                    is_remote = 'remote' in location.lower()
                    if settings.remote_only and not is_remote:
                        continue

                    job = Job(
                        title=title,
                        company=company,
                        company_info=get_company_info(company),
                        url=job_url,
                        location=location,
                        is_remote=is_remote
                    )
                    jobs.append(job)

                except Exception as e:
                    logger.error(f"Error parsing Greenhouse listing: {e}")

        except Exception as e:
            logger.error(f"Error fetching Greenhouse board for {company}: {e}")

        return jobs

    def _scrape_lever(self, company: str, keywords: List[str], max_jobs: int) -> List[Job]:
        """Scrape a Lever job board."""
        jobs = []
        company_slug = company.lower().replace(' ', '-')
        url = f"https://jobs.lever.co/{company_slug}"

        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            listings = soup.find_all('div', class_='posting')

            for listing in listings[:max_jobs]:
                try:
                    title_elem = listing.find('h5')
                    location_elem = listing.find('span', class_='location')
                    link_elem = listing.find('a', class_='posting-title')

                    if not all([title_elem, link_elem]):
                        continue

                    title = title_elem.text.strip()
                    location = location_elem.text.strip() if location_elem else "Unknown"
                    job_url = link_elem['href']

                    # Check keywords
                    title_lower = title.lower()
                    if not any(keyword.lower() in title_lower for keyword in keywords):
                        continue

                    # Check if remote
                    is_remote = 'remote' in location.lower()
                    if settings.remote_only and not is_remote:
                        continue

                    job = Job(
                        title=title,
                        company=company,
                        company_info=get_company_info(company),
                        url=job_url,
                        location=location,
                        is_remote=is_remote
                    )
                    jobs.append(job)

                except Exception as e:
                    logger.error(f"Error parsing Lever listing: {e}")

        except Exception as e:
            logger.error(f"Error fetching Lever board for {company}: {e}")

        return jobs


def get_all_scrapers() -> List[BaseScraper]:
    """Get all available scrapers."""
    return [
        RemoteOKScraper(),
        WWRScraper(),
        RemotiveScraper(),
        CompanyCareersPageScraper(),
    ]
