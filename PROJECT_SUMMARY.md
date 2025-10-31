# JobMiner - Project Summary

## 🎯 What You Got

A **complete, production-ready job scraper system** that automatically finds and filters senior tech jobs at established companies, running entirely for free using GitHub Actions and local LLM.

## 📦 What's Included

### Core Application
- ✅ **Python package** (`jobminer/`) with Poetry dependency management
- ✅ **Multi-source scraping**: RemoteOK, WeWorkRemotely, Remotive, company career pages
- ✅ **LLM filtering**: Local Ollama integration (llama2) to rank job relevance
- ✅ **Company database**: 80+ pre-vetted companies (200+ employees, 5+ years, stable)
- ✅ **Smart deduplication**: Merges results across runs
- ✅ **Multiple outputs**: JSON + CSV formats

### Automation
- ✅ **GitHub Actions workflow**: Runs daily at 9 AM UTC
- ✅ **Auto-commit results**: Updates data files automatically
- ✅ **Job summaries**: Visual reports in GitHub Actions UI
- ✅ **Manual trigger**: Can run on-demand

### Docker Support
- ✅ **Dockerfile**: Single-container setup
- ✅ **Docker Compose**: Multi-service with Ollama
- ✅ **Local testing**: Easy development environment

### Documentation
- ✅ **README.md**: Comprehensive guide (features, setup, config)
- ✅ **QUICKSTART.md**: 5-minute setup guide
- ✅ **CONTRIBUTING.md**: Developer guidelines
- ✅ **Issue templates**: For bugs, features, company additions

### Utilities
- ✅ **setup.sh**: Automated setup script
- ✅ **Makefile**: Convenient commands (run, clean, view, etc.)
- ✅ **analyze_jobs.py**: Stats and visualization tool
- ✅ **.env.example**: Configuration template

## 🎪 Target Jobs

**Roles:**
- Data Engineer
- Senior Data Engineer
- Software Engineer
- Solutions Architect

**Companies (Examples):**
- Cloud/Data: Snowflake, Databricks, MongoDB, Confluent, Elastic
- Big Tech: Microsoft, Amazon, Google, Meta, Netflix
- SaaS: Salesforce, ServiceNow, Workday, Atlassian
- FinTech: Stripe, Square, PayPal
- Security: CrowdStrike, Palo Alto Networks, Okta
- **80+ total companies**

**Requirements:**
- ✅ Remote positions
- ✅ 200+ employees
- ✅ 5+ years in business
- ✅ Stable growth
- ✅ Preference for public companies

## 🚀 How to Use

### Option 1: GitHub Actions (Zero Maintenance)
```bash
1. Fork repo
2. Enable Actions with write permissions
3. Push to trigger
→ Jobs auto-scraped daily, results committed to repo
```

### Option 2: Local Quick Run
```bash
./setup.sh          # One-time setup
ollama serve &      # Start LLM
poetry run jobminer # Run scraper
```

### Option 3: Docker
```bash
docker-compose up   # Everything included
```

## 📊 What You Get

After each run:
```
data/
├── jobs_latest.json          # All jobs (with scores)
├── jobs_latest.csv           # Excel-friendly format
├── jobs_YYYYMMDD_HHMMSS.json # Historical snapshots
└── result_*.json             # Run metadata
```

**Job Data Structure:**
```json
{
  "title": "Senior Data Engineer",
  "company": "Snowflake",
  "url": "https://...",
  "location": "Remote",
  "is_remote": true,
  "relevance_score": 0.95,
  "llm_analysis": "Excellent match because...",
  "scraped_at": "2024-10-31T12:00:00"
}
```

## 🔧 Key Features

### Smart Filtering
1. **Company Filter**: Only from your curated 80+ companies
2. **Role Filter**: Matches your target positions
3. **Remote Filter**: Remote-only if configured
4. **LLM Ranking**: 0.0-1.0 score based on your criteria
5. **Threshold**: Only saves jobs with score ≥ 0.5

### Data Quality
- Deduplication by URL
- Merges with historical data
- Keeps best scoring jobs
- Tracks when scraped

### Automation
- Runs on schedule (daily 9 AM UTC)
- Manual trigger available
- Auto-commits results
- Creates job summary reports
- Artifact upload for history

## 💰 Cost

**$0.00 / month**

Free tools used:
- GitHub Actions (2,000 min/month free)
- Ollama (local LLM, free)
- All scraping sources (free APIs)
- Docker (free)
- Poetry (free)

## 📈 Expected Results

**First run:**
- ~50-100 jobs found
- ~20-30 after LLM filtering
- Takes 5-10 minutes

**Daily runs:**
- New jobs added
- Deduplicated
- Historical data preserved

## 🎛️ Customization

Everything is configurable via `.env`:

```bash
# Change target roles
TARGET_ROLES=your,desired,roles

# Adjust company criteria
MIN_EMPLOYEES=300
MIN_YEARS_IN_BUSINESS=10

# LLM settings
OLLAMA_MODEL=mistral  # or codellama, llama2

# Output preferences
MAX_JOBS_PER_RUN=200
OUTPUT_FORMAT=json,csv
```

## 🛠️ Maintenance

**To add companies:**
Edit `jobminer/companies.py`

**To add job boards:**
Add scraper to `jobminer/scrapers/job_boards.py`

**To improve filtering:**
Edit prompts in `jobminer/llm_filter.py`

## 📁 File Structure

```
jobminer/
├── .github/
│   ├── workflows/scrape.yml      # GitHub Actions
│   └── ISSUE_TEMPLATE/           # Issue templates
├── jobminer/                     # Main package
│   ├── main.py                   # Entry point
│   ├── config.py                 # Settings
│   ├── models.py                 # Data models
│   ├── companies.py              # Company database ⭐
│   ├── llm_filter.py             # LLM integration
│   ├── scraper.py                # Orchestration
│   └── scrapers/
│       ├── base.py               # Base class
│       └── job_boards.py         # Scrapers ⭐
├── data/                         # Output directory
├── pyproject.toml                # Dependencies
├── Dockerfile                    # Docker image
├── docker-compose.yml            # Multi-container
├── setup.sh                      # Setup script
├── Makefile                      # Commands
├── analyze_jobs.py               # Analysis tool
├── .env.example                  # Config template
├── README.md                     # Full docs
├── QUICKSTART.md                 # Quick guide
└── CONTRIBUTING.md               # Dev guide
```

## 🎉 Next Steps

1. **Initial Setup:**
   ```bash
   cd jobminer
   ./setup.sh
   ```

2. **Local Test:**
   ```bash
   ollama serve &
   poetry run jobminer
   ./analyze_jobs.py
   ```

3. **View Results:**
   ```bash
   make view-latest
   # or
   open data/jobs_latest.csv
   ```

4. **GitHub Automation:**
   - Create GitHub repo
   - Push code
   - Enable Actions
   - Let it run automatically!

5. **Customize:**
   - Edit `.env` for preferences
   - Add companies to database
   - Adjust LLM prompts

## 🆘 Need Help?

- **Docs**: `README.md` (comprehensive)
- **Quick Start**: `QUICKSTART.md` (5-min guide)
- **Commands**: `make help`
- **Analysis**: `./analyze_jobs.py --help`

## 🎁 Bonus Features

- **Makefile commands**: `make view-latest`, `make check-ollama`
- **Analysis tool**: Stats, visualizations, export top jobs
- **GitHub Actions summary**: Visual job reports
- **Historical tracking**: Never lose a job posting
- **CSV export**: Easy Excel/Sheets import

## 🌟 You Now Have

✅ Automated job discovery
✅ AI-powered relevance filtering
✅ 80+ vetted companies
✅ Daily automated runs
✅ Zero ongoing costs
✅ Complete customization
✅ Professional codebase
✅ Full documentation

---

**Everything you need to find your next senior tech role!** 🚀

Start with: `./setup.sh` then `poetry run jobminer`

Or push to GitHub and let Actions handle everything!
