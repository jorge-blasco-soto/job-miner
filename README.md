# JobMiner 🔍💼

An automated job scraper for senior tech positions at well-established companies. JobMiner intelligently searches for remote data engineering, software engineering, and solutions architect roles at companies with 200+ employees, using a local LLM to filter and rank opportunities by relevance.

## Features

✨ **Automated Scraping**: Scrapes multiple job boards and company career pages daily
🤖 **LLM-Powered Filtering**: Uses local Ollama (free) or OpenAI-compatible APIs to rank jobs by relevance
🏢 **Curated Companies**: Pre-filtered list of 80+ established tech companies (200+ employees, 5+ years)
🔄 **GitHub Actions**: Fully automated via GitHub Actions - no server needed
🐳 **Docker Support**: Easy local testing with Docker Compose
📊 **Multiple Output Formats**: Saves results as JSON and CSV
🆓 **100% Free**: Uses only free tools and services

## Target Criteria

- **Roles**: Data Engineer, Senior Data Engineer, Software Engineer, Solutions Architect
- **Companies**: 200+ employees, 5+ years in business, stable growth
- **Location**: Remote positions only
- **Preference**: Public companies (but not restricted)
- **Industry**: IT & Software, Cloud/SaaS, Data Platforms

## Curated Companies

The system targets 80+ established companies including:
- **Cloud & Data**: Snowflake, Databricks, MongoDB, Confluent, Elastic
- **Major Tech**: Microsoft, Amazon, Google, Meta, Netflix, Adobe
- **SaaS Leaders**: Salesforce, ServiceNow, Workday, HubSpot
- **FinTech**: Stripe, Square, PayPal, Adyen
- **Cybersecurity**: CrowdStrike, Palo Alto Networks, Okta
- **And many more...**

See `jobminer/companies.py` for the full list.

## Quick Start

### Option 1: GitHub Actions (Recommended)

1. **Fork this repository**

2. **Enable GitHub Actions**
   - Go to your fork's Settings → Actions → General
   - Enable "Read and write permissions" for workflows

3. **Push to trigger**
   ```bash
   git commit --allow-empty -m "Trigger initial scrape"
   git push
   ```

4. **Check results**
   - Results are automatically committed to `data/jobs_latest.json` and `data/jobs_latest.csv`
   - Check the Actions tab for summaries and logs

The scraper runs automatically every day at 9 AM UTC, or you can trigger it manually from the Actions tab.

### Option 2: Local with Docker (Best for Testing)

1. **Install Docker and Docker Compose**

2. **Clone and setup**
   ```bash
   git clone <your-fork>
   cd jobminer
   cp .env.example .env
   ```

3. **Run with Docker Compose**
   ```bash
   docker-compose up
   ```

   This will:
   - Start Ollama service with llama2:7b model
   - Run the job scraper
   - Save results to `./data/`

### Option 3: Local with Poetry

1. **Install Poetry**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. **Install Ollama** (for local LLM)
   ```bash
   # macOS
   brew install ollama

   # Linux
   curl -fsSL https://ollama.com/install.sh | sh

   # Start Ollama
   ollama serve &
   ollama pull llama2
   ```

3. **Setup project**
   ```bash
   git clone <your-fork>
   cd jobminer
   poetry install
   cp .env.example .env
   ```

4. **Run the scraper**
   ```bash
   poetry run jobminer
   ```

## Configuration

Edit `.env` to customize behavior:

```bash
# LLM Configuration (local Ollama - recommended)
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama2

# Or use OpenAI-compatible API (optional)
# OPENAI_API_KEY=your_key_here
# OPENAI_MODEL=gpt-3.5-turbo

# Job Search Criteria
TARGET_ROLES=data engineer,senior data engineer,software engineer,solutions architect
MIN_EMPLOYEES=200
MIN_YEARS_IN_BUSINESS=5
REMOTE_ONLY=true
PREFER_PUBLIC_COMPANIES=true

# Scraping Settings
MAX_JOBS_PER_RUN=100
HEADLESS_BROWSER=true

# Output
DATA_DIR=./data
OUTPUT_FORMAT=json,csv
```

## Output Format

### JSON (`data/jobs_latest.json`)
```json
[
  {
    "id": "1234567890.123",
    "title": "Senior Data Engineer",
    "company": "Snowflake",
    "url": "https://...",
    "location": "Remote",
    "is_remote": true,
    "description": "...",
    "relevance_score": 0.95,
    "llm_analysis": "Excellent match - senior data engineering role...",
    "scraped_at": "2024-10-31T12:00:00"
  }
]
```

### CSV (`data/jobs_latest.csv`)
| title | company | url | location | is_remote | relevance_score | llm_analysis |
|-------|---------|-----|----------|-----------|-----------------|--------------|
| Senior Data Engineer | Snowflake | https://... | Remote | true | 0.95 | Excellent match... |

## How It Works

1. **Scraping**: Fetches jobs from multiple sources:
   - RemoteOK API
   - We Work Remotely
   - Remotive
   - Company career pages (Greenhouse, Lever)

2. **Filtering**:
   - Filters by company (must be in curated list)
   - Filters by role keywords
   - Filters by remote status

3. **LLM Analysis**:
   - Each job is analyzed by a local LLM (Ollama)
   - Scored 0.0-1.0 based on relevance to your criteria
   - Only jobs with score ≥ 0.5 are saved

4. **Deduplication**:
   - Merges with existing results
   - Removes duplicates by URL

5. **Storage**:
   - Saves to JSON and CSV
   - Keeps historical data
   - Updates `jobs_latest.*` files

## GitHub Actions Workflow

The automated workflow (`.github/workflows/scrape.yml`):
- ✅ Runs daily at 9 AM UTC
- ✅ Can be triggered manually
- ✅ Sets up Ollama with llama2 model
- ✅ Runs the scraper
- ✅ Commits results back to the repo
- ✅ Uploads artifacts
- ✅ Creates job summary in Actions UI

## Data Sources

- **RemoteOK**: Public API, no auth required
- **We Work Remotely**: Web scraping, programming category
- **Remotive**: Web scraping, software dev category
- **Company Career Pages**: Direct scraping of Greenhouse/Lever boards

All scraping is respectful with rate limiting and proper User-Agent headers.

## Customization

### Add More Companies

Edit `jobminer/companies.py` and add to the `ESTABLISHED_COMPANIES` list:

```python
{"name": "YourCompany", "employee_count": 500, "founded_year": 2015,
 "is_public": True, "industry": "Tech"},
```

### Add More Job Boards

Create a new scraper in `jobminer/scrapers/`:

```python
from jobminer.scrapers.base import BaseScraper

class YourScraper(BaseScraper):
    def scrape(self, keywords, max_jobs):
        # Your scraping logic
        return jobs
```

Add it to `get_all_scrapers()` in `jobminer/scrapers/job_boards.py`.

### Adjust LLM Filtering

Modify the prompt in `jobminer/llm_filter.py` to change how jobs are evaluated.

## Free Tools Used

- **Poetry**: Python dependency management
- **Ollama**: Free local LLM (llama2)
- **GitHub Actions**: Free CI/CD (2,000 minutes/month)
- **Docker**: Containerization
- **Beautiful Soup**: Web scraping
- **Requests**: HTTP client
- **Pydantic**: Data validation

## Troubleshooting

### No jobs found
- Check that Ollama is running: `curl http://localhost:11434/api/tags`
- Verify companies in `jobminer/companies.py` are currently hiring
- Check GitHub Actions logs for errors

### LLM errors
- Make sure Ollama is installed and running
- Pull the model: `ollama pull llama2`
- Check `.env` has correct `OLLAMA_BASE_URL`

### GitHub Actions fails
- Check workflow permissions (Settings → Actions → General)
- Verify the workflow file syntax
- Check Actions tab for detailed logs

## Project Structure

```
jobminer/
├── .github/
│   └── workflows/
│       └── scrape.yml          # GitHub Actions workflow
├── jobminer/
│   ├── __init__.py
│   ├── main.py                 # Entry point
│   ├── config.py               # Settings
│   ├── models.py               # Data models
│   ├── companies.py            # Company database
│   ├── llm_filter.py           # LLM integration
│   ├── scraper.py              # Orchestration
│   └── scrapers/
│       ├── __init__.py
│       ├── base.py             # Base scraper
│       └── job_boards.py       # Job board scrapers
├── data/                       # Output directory
├── pyproject.toml              # Poetry config
├── Dockerfile                  # Docker image
├── docker-compose.yml          # Docker Compose config
├── .env.example                # Example environment
└── README.md                   # This file
```

## Contributing

Feel free to:
- Add more companies to the database
- Implement new job board scrapers
- Improve LLM prompts
- Add features

## License

MIT License - feel free to use and modify!

## Disclaimer

This tool is for personal job searching purposes. Please respect:
- Websites' `robots.txt` and terms of service
- Rate limits and scraping policies
- Data privacy and GDPR compliance

Always review scraped data manually before applying.

---

**Happy job hunting! 🚀**

Found a great job using JobMiner? Let me know!
