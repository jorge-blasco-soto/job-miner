"""Data models for job scraping."""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, HttpUrl


class CompanySize(str, Enum):
    """Company size categories."""
    SMALL = "50-200"
    MEDIUM = "200-1000"
    LARGE = "1000-5000"
    ENTERPRISE = "5000+"


class JobLevel(str, Enum):
    """Job seniority levels."""
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    STAFF = "staff"
    PRINCIPAL = "principal"
    LEAD = "lead"


class Company(BaseModel):
    """Company information model."""
    name: str
    employee_count: Optional[int] = None
    founded_year: Optional[int] = None
    is_public: bool = False
    industry: Optional[str] = None
    revenue: Optional[str] = None
    growth_rate: Optional[str] = None
    headquarters: Optional[str] = None
    website: Optional[HttpUrl] = None

    @property
    def meets_criteria(self) -> bool:
        """Check if company meets the minimum criteria."""
        if self.employee_count and self.employee_count < 200:
            return False
        if self.founded_year:
            years_in_business = datetime.now().year - self.founded_year
            if years_in_business < 5:
                return False
        return True


class Job(BaseModel):
    """Job posting model."""
    id: str = Field(default_factory=lambda: f"{datetime.now().timestamp()}")
    title: str
    company: str
    company_info: Optional[Company] = None
    url: HttpUrl
    location: str
    is_remote: bool
    description: Optional[str] = None
    requirements: Optional[List[str]] = None
    posted_date: Optional[datetime] = None
    salary_range: Optional[str] = None
    job_level: Optional[JobLevel] = None

    # Scoring and filtering
    relevance_score: Optional[float] = None
    llm_analysis: Optional[str] = None
    scraped_at: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class ScrapingResult(BaseModel):
    """Result of a scraping session."""
    run_id: str
    timestamp: datetime = Field(default_factory=datetime.now)
    jobs_found: int = 0
    jobs_filtered: int = 0
    jobs_saved: int = 0
    errors: List[str] = Field(default_factory=list)
    sources: List[str] = Field(default_factory=list)
