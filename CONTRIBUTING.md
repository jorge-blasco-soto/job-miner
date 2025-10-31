# Contributing to JobMiner

Thank you for your interest in contributing to JobMiner! This document provides guidelines and instructions for contributing.

## Ways to Contribute

### 1. Add More Companies

The most valuable contribution is adding well-established companies to our database.

**Criteria for companies:**
- 200+ employees
- 5+ years in business
- Stable growth and revenue
- Active tech hiring
- Reputable in the industry

**How to add:**

Edit `jobminer/companies.py` and add to the `ESTABLISHED_COMPANIES` list:

```python
{
    "name": "CompanyName",
    "employee_count": 500,
    "founded_year": 2015,
    "is_public": True,  # or False
    "industry": "Category",
    "revenue": "Optional",
    "growth_rate": "Optional",
    "headquarters": "Optional",
    "website": "https://company.com"
}
```

### 2. Add New Job Board Scrapers

Create scrapers for additional job boards that focus on remote tech positions.

**Requirements:**
- Must be free to access
- Must have remote/tech jobs
- Should respect rate limits
- Must include proper error handling

**How to add:**

1. Create a new scraper class in `jobminer/scrapers/job_boards.py`:

```python
class NewBoardScraper(BaseScraper):
    def __init__(self):
        super().__init__("NewBoard")
        self.base_url = "https://..."

    def scrape(self, keywords: List[str], max_jobs: int = 50) -> List[Job]:
        # Implementation
        pass
```

2. Add it to `get_all_scrapers()` function

3. Test locally before submitting

### 3. Improve LLM Filtering

Enhance the LLM prompts or add new filtering strategies.

**Ideas:**
- Better job description analysis
- Salary range extraction
- Company culture matching
- Skills requirement parsing

### 4. Add Features

**Requested features:**
- Email notifications for new high-relevance jobs
- Slack/Discord webhook integration
- Job application tracking
- Cover letter generation
- Resume tailoring suggestions

### 5. Fix Bugs

Check the Issues tab for bugs to fix.

## Development Setup

1. **Fork and clone**
   ```bash
   git clone https://github.com/YOUR_USERNAME/jobminer.git
   cd jobminer
   ```

2. **Setup development environment**
   ```bash
   ./setup.sh
   # or
   make setup
   ```

3. **Install dev dependencies**
   ```bash
   poetry install --with dev
   ```

4. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Code Style

- Follow PEP 8
- Use type hints
- Add docstrings to functions
- Format with Black: `make format`
- Lint with flake8: `make lint`

## Testing

Before submitting:

1. **Test locally**
   ```bash
   poetry run jobminer
   ```

2. **Check output**
   ```bash
   make view-latest
   ```

3. **Lint code**
   ```bash
   make lint
   ```

4. **Format code**
   ```bash
   make format
   ```

## Submitting Changes

1. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add XYZ company to database"
   ```

2. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

3. **Create a Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Describe your changes
   - Submit!

## Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

Examples:
```
feat: add Stripe to company database
fix: handle missing job descriptions in scraper
docs: update setup instructions for Windows
```

## Code of Conduct

- Be respectful and professional
- Welcome newcomers
- Provide constructive feedback
- Focus on the code, not the person

## Questions?

Open an issue or discussion on GitHub!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
