"""Main entry point for the job scraper."""
import logging
import sys
from pathlib import Path

from jobminer.config import settings
from jobminer.scraper import JobScraperOrchestrator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('jobminer.log')
    ]
)

logger = logging.getLogger(__name__)


def main():
    """Main function to run the job scraper."""
    logger.info("=" * 80)
    logger.info("JobMiner - Automated Job Scraper")
    logger.info("=" * 80)

    try:
        # Create orchestrator and run
        orchestrator = JobScraperOrchestrator()
        result = orchestrator.run()

        # Print summary
        logger.info("=" * 80)
        logger.info("SCRAPING SUMMARY")
        logger.info("=" * 80)
        logger.info(f"Run ID: {result.run_id}")
        logger.info(f"Jobs Found: {result.jobs_found}")
        logger.info(f"Jobs Filtered: {result.jobs_filtered}")
        logger.info(f"Jobs Saved: {result.jobs_saved}")
        logger.info(f"Sources: {', '.join(result.sources)}")

        if result.errors:
            logger.warning(f"Errors encountered: {len(result.errors)}")
            for error in result.errors:
                logger.warning(f"  - {error}")

        logger.info("=" * 80)
        logger.info(f"Results saved to: {settings.data_dir}")
        logger.info("Check jobs_latest.json or jobs_latest.csv for the latest results")
        logger.info("=" * 80)

        return 0

    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
