"""Scraper orchestration and data management."""
import csv
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import List

from jobminer.config import settings
from jobminer.llm_filter import build_user_criteria, get_llm_filter
from jobminer.models import Job, ScrapingResult
from jobminer.scrapers.job_boards import get_all_scrapers

logger = logging.getLogger(__name__)


class JobScraperOrchestrator:
    """Orchestrates the job scraping process."""

    def __init__(self, data_dir: Path = None):
        self.data_dir = data_dir or settings.data_dir
        self.data_dir.mkdir(exist_ok=True, parents=True)
        self.scrapers = get_all_scrapers()
        self.llm_filter = get_llm_filter()

    def run(self) -> ScrapingResult:
        """Run the complete scraping pipeline."""
        run_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        result = ScrapingResult(run_id=run_id)

        logger.info(f"Starting scraping run: {run_id}")

        # Step 1: Scrape jobs from all sources
        all_jobs = []
        keywords = settings.target_roles_list

        for scraper in self.scrapers:
            try:
                logger.info(f"Scraping from {scraper.name}...")
                jobs = scraper.scrape(keywords, max_jobs=settings.max_jobs_per_run // len(self.scrapers))
                all_jobs.extend(jobs)
                result.sources.append(scraper.name)
            except Exception as e:
                error_msg = f"Error with {scraper.name}: {str(e)}"
                logger.error(error_msg)
                result.errors.append(error_msg)

        result.jobs_found = len(all_jobs)
        logger.info(f"Total jobs found: {result.jobs_found}")

        if not all_jobs:
            logger.warning("No jobs found!")
            return result

        # Step 2: Deduplicate
        all_jobs = self._deduplicate(all_jobs)
        logger.info(f"Jobs after deduplication: {len(all_jobs)}")

        # Step 3: Filter with LLM
        if self.llm_filter:
            try:
                logger.info("Filtering jobs with LLM...")
                user_criteria = build_user_criteria()
                all_jobs = self.llm_filter.batch_analyze(all_jobs, user_criteria)

                # Keep jobs with score >= 0.5
                filtered_jobs = [job for job in all_jobs if job.relevance_score and job.relevance_score >= 0.5]
                result.jobs_filtered = len(filtered_jobs)

                # Sort by relevance score
                filtered_jobs.sort(key=lambda x: x.relevance_score or 0, reverse=True)

                logger.info(f"Jobs after LLM filtering: {result.jobs_filtered}")
            except Exception as e:
                error_msg = f"LLM filtering error: {str(e)}"
                logger.error(error_msg)
                result.errors.append(error_msg)
                filtered_jobs = all_jobs  # Use unfiltered if LLM fails
        else:
            logger.warning("No LLM filter available, saving all jobs")
            filtered_jobs = all_jobs
            result.jobs_filtered = len(filtered_jobs)

        # Step 4: Load existing jobs and merge
        existing_jobs = self._load_existing_jobs()
        merged_jobs = self._merge_with_existing(filtered_jobs, existing_jobs)

        # Step 5: Save results
        result.jobs_saved = len(merged_jobs)
        self._save_jobs(merged_jobs, run_id)
        self._save_result(result)

        logger.info(f"Scraping complete. Saved {result.jobs_saved} jobs.")
        return result

    def _deduplicate(self, jobs: List[Job]) -> List[Job]:
        """Remove duplicate jobs based on URL."""
        seen_urls = set()
        unique_jobs = []
        for job in jobs:
            url_str = str(job.url)
            if url_str not in seen_urls:
                seen_urls.add(url_str)
                unique_jobs.append(job)
        return unique_jobs

    def _load_existing_jobs(self) -> List[Job]:
        """Load existing jobs from the latest file."""
        existing_jobs = []

        # Find most recent jobs file
        json_files = sorted(self.data_dir.glob("jobs_*.json"), reverse=True)
        if not json_files:
            return existing_jobs

        try:
            with open(json_files[0], 'r') as f:
                data = json.load(f)
                existing_jobs = [Job(**job_data) for job_data in data]
            logger.info(f"Loaded {len(existing_jobs)} existing jobs")
        except Exception as e:
            logger.error(f"Error loading existing jobs: {e}")

        return existing_jobs

    def _merge_with_existing(self, new_jobs: List[Job], existing_jobs: List[Job]) -> List[Job]:
        """Merge new jobs with existing, avoiding duplicates."""
        existing_urls = {str(job.url) for job in existing_jobs}

        # Add new jobs that don't exist
        for job in new_jobs:
            if str(job.url) not in existing_urls:
                existing_jobs.append(job)

        # Sort by scraped date
        existing_jobs.sort(key=lambda x: x.scraped_at, reverse=True)

        return existing_jobs

    def _save_jobs(self, jobs: List[Job], run_id: str):
        """Save jobs to configured output formats."""
        # Save as JSON
        if "json" in settings.output_formats:
            json_file = self.data_dir / f"jobs_{run_id}.json"
            with open(json_file, 'w') as f:
                json.dump(
                    [job.model_dump(mode='json') for job in jobs],
                    f,
                    indent=2,
                    default=str
                )
            logger.info(f"Saved jobs to {json_file}")

            # Also save to a 'latest' file for easy access
            latest_file = self.data_dir / "jobs_latest.json"
            with open(latest_file, 'w') as f:
                json.dump(
                    [job.model_dump(mode='json') for job in jobs],
                    f,
                    indent=2,
                    default=str
                )

        # Save as CSV
        if "csv" in settings.output_formats:
            csv_file = self.data_dir / f"jobs_{run_id}.csv"
            with open(csv_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'title', 'company', 'url', 'location', 'is_remote',
                    'relevance_score', 'llm_analysis', 'posted_date', 'scraped_at'
                ])
                writer.writeheader()
                for job in jobs:
                    writer.writerow({
                        'title': job.title,
                        'company': job.company,
                        'url': str(job.url),
                        'location': job.location,
                        'is_remote': job.is_remote,
                        'relevance_score': job.relevance_score,
                        'llm_analysis': job.llm_analysis,
                        'posted_date': job.posted_date,
                        'scraped_at': job.scraped_at,
                    })
            logger.info(f"Saved jobs to {csv_file}")

            # Also save to a 'latest' file
            latest_csv = self.data_dir / "jobs_latest.csv"
            with open(latest_csv, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'title', 'company', 'url', 'location', 'is_remote',
                    'relevance_score', 'llm_analysis', 'posted_date', 'scraped_at'
                ])
                writer.writeheader()
                for job in jobs:
                    writer.writerow({
                        'title': job.title,
                        'company': job.company,
                        'url': str(job.url),
                        'location': job.location,
                        'is_remote': job.is_remote,
                        'relevance_score': job.relevance_score,
                        'llm_analysis': job.llm_analysis,
                        'posted_date': job.posted_date,
                        'scraped_at': job.scraped_at,
                    })

    def _save_result(self, result: ScrapingResult):
        """Save scraping result metadata."""
        result_file = self.data_dir / f"result_{result.run_id}.json"
        with open(result_file, 'w') as f:
            json.dump(result.model_dump(mode='json'), f, indent=2, default=str)
