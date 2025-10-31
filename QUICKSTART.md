# Quick Start Guide

## 🚀 5-Minute Setup (Local)

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd jobminer

# 2. Run the setup script
chmod +x setup.sh
./setup.sh

# 3. Start Ollama (in a separate terminal)
ollama serve

# 4. Run the scraper
poetry run jobminer
# or
make run

# 5. View results
cat data/jobs_latest.json
# or
make view-latest
```

## ☁️ GitHub Actions Setup (Automated)

```bash
# 1. Fork this repository on GitHub

# 2. Clone your fork
git clone https://github.com/YOUR_USERNAME/jobminer.git
cd jobminer

# 3. Enable Actions
# Go to: Settings → Actions → General
# Enable: "Read and write permissions"

# 4. Push to trigger
git commit --allow-empty -m "Trigger scraper"
git push

# 5. Check results
# Go to: Actions tab (see logs)
# Results auto-committed to: data/jobs_latest.json
```

Jobs are automatically scraped daily at 9 AM UTC!

## 🐳 Docker Setup

```bash
# Run everything with Docker Compose
docker-compose up

# Results saved to ./data/
```

## 📊 Viewing Results

### JSON
```bash
cat data/jobs_latest.json | python3 -m json.tool
```

### CSV (opens in Excel)
```bash
open data/jobs_latest.csv
```

### Top 10 by relevance
```bash
make view-latest
```

## ⚙️ Configuration

Edit `.env`:
```bash
# Change target roles
TARGET_ROLES=your,desired,roles

# Adjust filters
MIN_EMPLOYEES=300
REMOTE_ONLY=true

# Change LLM model
OLLAMA_MODEL=mistral  # or codellama, llama2, etc.
```

## 🛠️ Common Commands

```bash
make help          # Show all commands
make setup         # Initial setup
make run           # Run scraper
make view-latest   # View results
make check-ollama  # Check LLM status
make clean         # Clean temp files
```

## 🔧 Troubleshooting

### "No jobs found"
- Companies may not be actively hiring
- Check GitHub Actions logs for errors
- Verify company names in `jobminer/companies.py`

### "Ollama connection error"
```bash
# Start Ollama
ollama serve

# Check it's running
curl http://localhost:11434/api/tags

# Pull model if needed
ollama pull llama2
```

### "Module not found"
```bash
# Reinstall dependencies
poetry install
```

### GitHub Actions fails
- Check workflow permissions in Settings
- Verify `.github/workflows/scrape.yml` syntax
- Check Actions logs for details

## 📈 What to Expect

**First run:**
- 50-100 jobs found
- ~20-30 after LLM filtering (score ≥ 0.5)
- Takes 5-10 minutes

**Daily runs:**
- Merges with existing jobs
- Deduplicates by URL
- Keeps historical data

## 🎯 Next Steps

1. **Review results**: Check `data/jobs_latest.csv`
2. **Customize**: Edit `.env` for your preferences
3. **Add companies**: Edit `jobminer/companies.py`
4. **Set up GitHub Actions**: For daily automation
5. **Apply**: Use the links in the output!

## 💡 Pro Tips

- Sort CSV by `relevance_score` column
- Read `llm_analysis` for quick insights
- Check `scraped_at` for freshness
- Add your own companies to track
- Adjust `MIN_EMPLOYEES` to broaden search

## 📚 More Info

- Full docs: `README.md`
- Contributing: `CONTRIBUTING.md`
- Issues: GitHub Issues tab

---

**Happy job hunting! 🎉**
