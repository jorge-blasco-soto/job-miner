# 🚀 Getting Started Checklist

Use this checklist to get JobMiner up and running!

## ✅ Local Setup (Recommended for Testing)

### Prerequisites
- [ ] Python 3.10+ installed (`python3 --version`)
- [ ] Git installed (`git --version`)

### Setup Steps
- [ ] Navigate to project: `cd jobminer`
- [ ] Run setup script: `./setup.sh`
- [ ] Verify `.env` file exists
- [ ] Verify `data/` directory exists

### Install Ollama (Local LLM)
- [ ] **macOS**: `brew install ollama`
- [ ] **Linux**: `curl -fsSL https://ollama.com/install.sh | sh`
- [ ] Start Ollama: `ollama serve` (keep running in terminal)
- [ ] Pull model: `ollama pull llama2`
- [ ] Verify: `curl http://localhost:11434/api/tags`

### First Run
- [ ] Open new terminal (keep Ollama running in first)
- [ ] Run scraper: `poetry run jobminer`
- [ ] Wait 5-10 minutes for completion
- [ ] Check results: `cat data/jobs_latest.json`
- [ ] View analysis: `./analyze_jobs.py`

### Verify Results
- [ ] `data/jobs_latest.json` exists
- [ ] `data/jobs_latest.csv` exists
- [ ] Jobs have `relevance_score` field
- [ ] Jobs are from companies in `jobminer/companies.py`

---

## ☁️ GitHub Actions Setup (Recommended for Automation)

### GitHub Setup
- [ ] Create GitHub account (if needed)
- [ ] Create new repository on GitHub
- [ ] Name it (e.g., "jobminer" or "job-scraper")
- [ ] Set to Public or Private (your choice)
- [ ] **Don't** initialize with README (we have one)

### Local Git Setup
- [ ] In project directory: `git init`
- [ ] Add remote: `git remote add origin <your-repo-url>`
- [ ] Stage files: `git add .`
- [ ] Commit: `git commit -m "Initial commit: JobMiner setup"`
- [ ] Push: `git push -u origin main`

### Enable GitHub Actions
- [ ] Go to your repo on GitHub
- [ ] Click **Settings**
- [ ] Click **Actions** → **General**
- [ ] Under "Workflow permissions":
  - [ ] Select **Read and write permissions**
  - [ ] Check **Allow GitHub Actions to create and approve pull requests**
- [ ] Click **Save**

### Trigger First Run
- [ ] Go to **Actions** tab
- [ ] Click **Job Scraper** workflow
- [ ] Click **Run workflow** dropdown
- [ ] Click green **Run workflow** button
- [ ] Wait for completion (~10 minutes)

### Verify GitHub Actions
- [ ] Workflow completed successfully (green checkmark)
- [ ] Check **Summary** for job statistics
- [ ] Go to **Code** tab
- [ ] Verify `data/jobs_latest.json` exists
- [ ] Verify `data/jobs_latest.csv` exists
- [ ] Open files to see job results

### Automatic Runs
- [ ] Workflow will now run daily at 9 AM UTC
- [ ] Results auto-committed to repo
- [ ] Check **Actions** tab for run history

---

## 🐳 Docker Setup (Alternative)

### Prerequisites
- [ ] Docker installed (`docker --version`)
- [ ] Docker Compose installed (`docker-compose --version`)

### Run with Docker
- [ ] Navigate to project: `cd jobminer`
- [ ] Start services: `docker-compose up`
- [ ] Wait for completion
- [ ] Check `data/` directory for results

---

## 🎯 Customization

### Edit Configuration
- [ ] Open `.env` file
- [ ] Customize `TARGET_ROLES` (your desired job titles)
- [ ] Adjust `MIN_EMPLOYEES` (company size preference)
- [ ] Set `REMOTE_ONLY` (true/false)
- [ ] Change `MAX_JOBS_PER_RUN` (number of jobs to fetch)
- [ ] Save changes

### Add More Companies
- [ ] Open `jobminer/companies.py`
- [ ] Add companies to `ESTABLISHED_COMPANIES` list
- [ ] Follow existing format
- [ ] Save file
- [ ] Re-run scraper

### Change LLM Model
- [ ] See available models: `ollama list`
- [ ] Pull new model: `ollama pull mistral`
- [ ] Update `.env`: `OLLAMA_MODEL=mistral`
- [ ] Re-run scraper

---

## 📊 Using Results

### View Results
- [ ] **JSON**: `cat data/jobs_latest.json | python3 -m json.tool`
- [ ] **CSV**: `open data/jobs_latest.csv` (Excel/Numbers)
- [ ] **Analysis**: `./analyze_jobs.py`
- [ ] **Top jobs**: `make view-latest`

### Sort and Filter
- [ ] Open CSV in Excel/Google Sheets
- [ ] Sort by `relevance_score` (highest first)
- [ ] Filter by `company` or `title`
- [ ] Click URLs to apply

### Export Top Jobs
- [ ] Run: `./analyze_jobs.py --export --min-score 0.8`
- [ ] Creates: `data/top_jobs.json`
- [ ] Only jobs with score ≥ 0.8

---

## 🔧 Troubleshooting

### No jobs found
- [ ] Check Ollama is running: `curl http://localhost:11434/api/tags`
- [ ] Verify companies in database are hiring
- [ ] Check `jobminer.log` for errors
- [ ] Try increasing `MAX_JOBS_PER_RUN` in `.env`

### Ollama errors
- [ ] Make sure Ollama is running: `ollama serve`
- [ ] Check model is pulled: `ollama list`
- [ ] Try different model: `ollama pull mistral`
- [ ] Verify URL in `.env`: `OLLAMA_BASE_URL=http://localhost:11434`

### GitHub Actions fails
- [ ] Check workflow permissions are enabled
- [ ] View error logs in Actions tab
- [ ] Verify `.github/workflows/scrape.yml` syntax
- [ ] Check for rate limiting issues

### Import errors
- [ ] Reinstall dependencies: `poetry install`
- [ ] Check Python version: `python3 --version` (need 3.10+)
- [ ] Activate environment: `poetry shell`

---

## 🎓 Learning More

### Documentation
- [ ] Read `README.md` - Full documentation
- [ ] Read `QUICKSTART.md` - Quick reference
- [ ] Read `CONTRIBUTING.md` - How to contribute
- [ ] Read `PROJECT_SUMMARY.md` - What you have

### Useful Commands
- [ ] `make help` - Show all make commands
- [ ] `make check-ollama` - Check LLM status
- [ ] `make view-latest` - View recent jobs
- [ ] `make clean` - Clean temp files
- [ ] `./analyze_jobs.py --help` - Analysis options

---

## ✨ Success Criteria

You'll know it's working when:
- [ ] ✅ Scraper runs without errors
- [ ] ✅ `data/jobs_latest.json` has jobs (20-50+)
- [ ] ✅ Jobs have `relevance_score` values
- [ ] ✅ Jobs are from established companies
- [ ] ✅ Jobs match your target roles
- [ ] ✅ CSV file opens in Excel/Sheets
- [ ] ✅ (Optional) GitHub Actions runs daily

---

## 🆘 Still Stuck?

1. Check `jobminer.log` file
2. Run with verbose output: `poetry run python -m jobminer.main`
3. Check GitHub Issues (if using repo)
4. Review error messages carefully
5. Try Docker method as alternative

---

## 🎉 Next Steps After Setup

1. **Review Results**: Open `data/jobs_latest.csv`, sort by score
2. **Apply to Jobs**: Click URLs, submit applications
3. **Customize**: Add your favorite companies
4. **Automate**: Set up GitHub Actions for daily runs
5. **Track**: Use CSV to track applications

---

**Ready to find your next role? Start with: `./setup.sh`** 🚀
