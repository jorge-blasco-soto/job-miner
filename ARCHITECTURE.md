# JobMiner Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         JOBMINER SYSTEM                          │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  Trigger Source  │
└────────┬─────────┘
         │
         ├─ Manual: poetry run jobminer
         ├─ Automated: GitHub Actions (daily 9 AM UTC)
         └─ Docker: docker-compose up
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                      JOB SCRAPER ORCHESTRATOR                    │
│                       (jobminer/scraper.py)                      │
└────────┬────────────────────────────────────────────────────────┘
         │
         ▼
    ┌────────────────────────────────────┐
    │  STEP 1: Scrape from Multiple      │
    │          Job Sources               │
    └────┬───────────────────────────────┘
         │
         ├─ RemoteOK API         ──────> Public API (no auth)
         ├─ We Work Remotely     ──────> Web scraping
         ├─ Remotive             ──────> Web scraping
         └─ Company Career Pages ──────> Greenhouse/Lever boards
         │
         ▼
    ┌────────────────────────────────────┐
    │  STEP 2: Filter by Company         │
    │          (80+ established cos)     │
    └────┬───────────────────────────────┘
         │
         │  Companies Database (jobminer/companies.py)
         │  ├─ 200+ employees ✓
         │  ├─ 5+ years old ✓
         │  ├─ Stable growth ✓
         │  └─ Tech-focused ✓
         │
         ▼
    ┌────────────────────────────────────┐
    │  STEP 3: Filter by Keywords        │
    │          & Remote Status           │
    └────┬───────────────────────────────┘
         │
         │  Target Roles:
         │  ├─ Data Engineer
         │  ├─ Senior Data Engineer
         │  ├─ Software Engineer
         │  └─ Solutions Architect
         │
         ▼
    ┌────────────────────────────────────┐
    │  STEP 4: Deduplicate by URL        │
    └────┬───────────────────────────────┘
         │
         ▼
    ┌────────────────────────────────────┐
    │  STEP 5: LLM Analysis & Scoring    │
    │          (jobminer/llm_filter.py)  │
    └────┬───────────────────────────────┘
         │
         ├─ Ollama (Local) ──> llama2 model
         │  └─ FREE, runs locally
         │
         └─ OpenAI API (Optional) ──> gpt-3.5-turbo
            └─ For cloud deployment
         │
         │  For each job:
         │  ├─ Analyze description
         │  ├─ Match to criteria
         │  ├─ Generate score (0.0-1.0)
         │  └─ Write explanation
         │
         ▼
    ┌────────────────────────────────────┐
    │  STEP 6: Filter by Score ≥ 0.5     │
    └────┬───────────────────────────────┘
         │
         ▼
    ┌────────────────────────────────────┐
    │  STEP 7: Merge with Existing       │
    │          (avoid duplicates)        │
    └────┬───────────────────────────────┘
         │
         ▼
    ┌────────────────────────────────────┐
    │  STEP 8: Save Results              │
    └────┬───────────────────────────────┘
         │
         ├─ data/jobs_latest.json  (all jobs)
         ├─ data/jobs_latest.csv   (spreadsheet)
         ├─ data/jobs_TIMESTAMP.*  (historical)
         └─ data/result_*.json     (metadata)
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         OUTPUT & DELIVERY                        │
└─────────────────────────────────────────────────────────────────┘
         │
         ├─ Local: Files in data/ directory
         ├─ GitHub: Auto-committed to repository
         └─ Actions: Summary in GitHub UI
```

## Data Flow Diagram

```
┌─────────────┐
│ Job Sources │
└──────┬──────┘
       │
       │ Raw job listings
       ▼
┌──────────────────┐      ┌──────────────────┐
│ Company Filter   │ ◀─── │ Company Database │
└──────┬───────────┘      └──────────────────┘
       │                   (80+ companies)
       │ Filtered jobs
       ▼
┌──────────────────┐      ┌──────────────────┐
│ Keyword Filter   │ ◀─── │ Target Roles     │
└──────┬───────────┘      └──────────────────┘
       │                   (config.py)
       │ Matched jobs
       ▼
┌──────────────────┐      ┌──────────────────┐
│   LLM Analyzer   │ ◀─── │ Ollama / OpenAI  │
└──────┬───────────┘      └──────────────────┘
       │                   (Local or Cloud)
       │ Scored jobs
       ▼
┌──────────────────┐
│ Score Filter     │
│   (≥ 0.5)        │
└──────┬───────────┘
       │ Relevant jobs
       ▼
┌──────────────────┐      ┌──────────────────┐
│ Deduplicator     │ ◀─── │ Existing Jobs    │
└──────┬───────────┘      └──────────────────┘
       │                   (previous runs)
       │ Unique jobs
       ▼
┌──────────────────┐
│  Storage Layer   │
│  - JSON          │
│  - CSV           │
└──────────────────┘
```

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         JOBMINER PACKAGE                         │
└─────────────────────────────────────────────────────────────────┘

jobminer/
│
├─ main.py ─────────────────┐
│  └─ Entry point, logging  │
│                            ▼
├─ config.py ───────────────────┐ Settings & Environment
│  └─ Pydantic settings         │ - Target roles
│                                │ - Min employees/years
│                                │ - LLM config
│                                │ - Output format
│                                │
├─ models.py ───────────────────┤ Data Models
│  ├─ Job                        │ - Job schema
│  ├─ Company                    │ - Company schema
│  └─ ScrapingResult             │ - Result metadata
│                                │
├─ companies.py ────────────────┤ Company Database
│  ├─ ESTABLISHED_COMPANIES      │ - 80+ companies
│  ├─ get_companies()            │ - Lookup functions
│  └─ is_established_company()   │ - Validation
│                                │
├─ scrapers/ ───────────────────┤ Scraping Module
│  ├─ base.py                    │ - BaseScraper class
│  │  └─ Abstract scraper        │ - Common methods
│  │                              │
│  └─ job_boards.py              │ - Implementations
│     ├─ RemoteOKScraper         │   - RemoteOK API
│     ├─ WWRScraper              │   - We Work Remotely
│     ├─ RemotiveScraper         │   - Remotive
│     └─ CompanyCareersPage      │   - Greenhouse/Lever
│                                │
├─ llm_filter.py ───────────────┤ LLM Integration
│  ├─ LLMFilter (base)           │ - Base class
│  ├─ OllamaFilter               │ - Local Ollama
│  ├─ OpenAICompatibleFilter     │ - Cloud API
│  └─ get_llm_filter()           │ - Factory
│                                │
└─ scraper.py ──────────────────┘ Orchestration
   └─ JobScraperOrchestrator     - Coordinates all steps
      ├─ run()                    - Main pipeline
      ├─ _deduplicate()           - Remove dupes
      ├─ _merge_with_existing()   - Merge data
      └─ _save_jobs()             - Persist results
```

## Automation Flow (GitHub Actions)

```
┌─────────────────────────────────────────────────────────────────┐
│                     GITHUB ACTIONS WORKFLOW                      │
│                 (.github/workflows/scrape.yml)                   │
└─────────────────────────────────────────────────────────────────┘

Trigger:
  ├─ Schedule: Daily at 9 AM UTC (cron)
  ├─ Manual: workflow_dispatch
  └─ Push: to main branch

Steps:
  │
  1. Checkout code ────────────> actions/checkout@v4
  │
  2. Setup Python ─────────────> python 3.11
  │
  3. Install Poetry ───────────> snok/install-poetry
  │
  4. Cache dependencies ───────> actions/cache (venv)
  │
  5. Install dependencies ─────> poetry install
  │
  6. Setup Ollama ─────────────┐
  │  ├─ Download & install      │
  │  ├─ Start service           │
  │  └─ Pull llama2 model       │
  │                             │
  7. Configure environment ────┤ Create .env
  │                             │
  8. Run scraper ──────────────> poetry run jobminer
  │                             │
  9. Commit results ───────────┐
  │  ├─ Add data files          │
  │  ├─ Commit changes          │
  │  └─ Push to repo            │
  │                             │
 10. Upload artifacts ─────────┐
  │  ├─ jobs_latest.json        │
  │  ├─ jobs_latest.csv         │
  │  └─ jobminer.log            │
  │                             │
 11. Create summary ───────────┐
     └─ Show stats in UI        │
        ├─ Total jobs           │
        ├─ Top companies        │
        └─ Best matches         │

Output:
  ├─ Committed to repository
  ├─ Artifacts (30 days)
  └─ Visual summary
```

## Technology Stack

```
┌─────────────────────────────────────────────────────────────────┐
│                        TECHNOLOGY STACK                          │
└─────────────────────────────────────────────────────────────────┘

Language & Runtime:
  ├─ Python 3.10+
  └─ Poetry (dependency management)

Web Scraping:
  ├─ requests (HTTP client)
  ├─ BeautifulSoup4 (HTML parsing)
  └─ lxml (XML/HTML parser)

Data Processing:
  ├─ Pydantic (data validation)
  ├─ Pydantic Settings (config)
  └─ JSON/CSV (storage)

LLM Integration:
  ├─ Ollama (local, FREE)
  │  └─ llama2, mistral, codellama
  └─ OpenAI SDK (cloud, optional)
     └─ gpt-3.5-turbo, gpt-4

Automation:
  ├─ GitHub Actions (CI/CD)
  └─ Cron scheduling

Containerization:
  ├─ Docker
  └─ Docker Compose

Development:
  ├─ Black (formatting)
  ├─ flake8 (linting)
  ├─ mypy (type checking)
  └─ pytest (testing)

All 100% FREE & Open Source! 🎉
```

## Deployment Options

```
Option 1: GitHub Actions (Recommended)
  ✅ Completely automated
  ✅ Free (2,000 min/month)
  ✅ Results auto-committed
  ✅ No server needed
  ❌ Slower LLM (runs in cloud)

Option 2: Local Execution
  ✅ Fast LLM (local Ollama)
  ✅ Immediate results
  ✅ Full control
  ❌ Manual execution
  ❌ Requires local setup

Option 3: Docker
  ✅ Consistent environment
  ✅ Easy setup
  ✅ Portable
  ❌ Requires Docker installed
  ❌ More resource intensive

Choose based on your needs!
```
