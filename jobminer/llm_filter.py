"""LLM integration for job filtering and analysis."""
import json
import logging
from typing import List, Optional

from jobminer.config import settings
from jobminer.models import Job

logger = logging.getLogger(__name__)


class LLMFilter:
    """Base class for LLM-based job filtering."""

    def __init__(self):
        self.model = None

    def analyze_job(self, job: Job, user_criteria: str) -> tuple[float, str]:
        """
        Analyze a job posting and return a relevance score and analysis.

        Args:
            job: Job posting to analyze
            user_criteria: User's job search criteria

        Returns:
            Tuple of (relevance_score, analysis_text)
        """
        raise NotImplementedError

    def batch_analyze(self, jobs: List[Job], user_criteria: str) -> List[Job]:
        """Analyze multiple jobs and update their relevance scores."""
        for job in jobs:
            try:
                score, analysis = self.analyze_job(job, user_criteria)
                job.relevance_score = score
                job.llm_analysis = analysis
            except Exception as e:
                logger.error(f"Error analyzing job {job.id}: {e}")
                job.relevance_score = 0.0
                job.llm_analysis = f"Error during analysis: {str(e)}"
        return jobs


class OllamaFilter(LLMFilter):
    """LLM filter using local Ollama instance (free)."""

    def __init__(self):
        super().__init__()
        try:
            import ollama
            self.client = ollama.Client(host=settings.ollama_base_url)
            self.model = settings.ollama_model
            logger.info(f"Initialized Ollama filter with model: {self.model}")
        except ImportError:
            logger.error("Ollama package not installed. Install with: pip install ollama")
            raise
        except Exception as e:
            logger.error(f"Error initializing Ollama: {e}")
            raise

    def analyze_job(self, job: Job, user_criteria: str) -> tuple[float, str]:
        """Analyze job using Ollama."""
        prompt = f"""Analyze this job posting and rate its relevance for the candidate.

User's Criteria:
{user_criteria}

Job Details:
- Title: {job.title}
- Company: {job.company}
- Location: {job.location}
- Remote: {job.is_remote}
- Description: {job.description[:500] if job.description else 'N/A'}

Please provide:
1. A relevance score from 0.0 to 1.0 (where 1.0 is perfect match)
2. A brief explanation of why this job matches or doesn't match the criteria

Respond in JSON format:
{{"score": 0.0-1.0, "analysis": "your analysis here"}}
"""

        try:
            response = self.client.generate(
                model=self.model,
                prompt=prompt,
                format='json'
            )

            result = json.loads(response['response'])
            score = float(result.get('score', 0.0))
            analysis = result.get('analysis', 'No analysis provided')

            return score, analysis

        except Exception as e:
            logger.error(f"Ollama analysis error: {e}")
            return 0.0, f"Analysis failed: {str(e)}"


class OpenAICompatibleFilter(LLMFilter):
    """LLM filter using OpenAI-compatible API (for small/free models)."""

    def __init__(self, api_key: str = None, base_url: str = None, model: str = None):
        super().__init__()
        try:
            from openai import OpenAI

            # Use provided values or fall back to settings
            api_key = api_key or settings.openai_api_key
            if not api_key:
                raise ValueError("API key not configured")

            self.client = OpenAI(
                api_key=api_key,
                base_url=base_url or settings.openai_base_url
            )
            self.model = model or settings.openai_model
            logger.info(f"Initialized OpenAI-compatible filter with model: {self.model}")
        except ImportError:
            logger.error("OpenAI package not installed. Install with: pip install openai")
            raise
        except Exception as e:
            logger.error(f"Error initializing OpenAI client: {e}")
            raise

    def analyze_job(self, job: Job, user_criteria: str) -> tuple[float, str]:
        """Analyze job using OpenAI-compatible API."""
        prompt = f"""Analyze this job posting and rate its relevance for the candidate.

User's Criteria:
{user_criteria}

Job Details:
- Title: {job.title}
- Company: {job.company}
- Location: {job.location}
- Remote: {job.is_remote}
- Description: {job.description[:500] if job.description else 'N/A'}

Provide a relevance score from 0.0 to 1.0 and a brief explanation.
Respond in JSON: {{"score": 0.0-1.0, "analysis": "explanation"}}
"""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a job matching assistant. Respond only with JSON."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )

            result = json.loads(response.choices[0].message.content)
            score = float(result.get('score', 0.0))
            analysis = result.get('analysis', 'No analysis provided')

            return score, analysis

        except Exception as e:
            logger.error(f"OpenAI API analysis error: {e}")
            return 0.0, f"Analysis failed: {str(e)}"


class GroqFilter(OpenAICompatibleFilter):
    """LLM filter using Groq's free API (OpenAI-compatible)."""

    def __init__(self):
        if not settings.groq_api_key:
            raise ValueError("Groq API key not configured. Get one free at https://console.groq.com")

        super().__init__(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
            model=settings.groq_model
        )
        logger.info(f"Initialized Groq filter with model: {self.model} (FREE)")


def get_llm_filter() -> Optional[LLMFilter]:
    """Get the appropriate LLM filter based on configuration."""
    # Try Groq first (free cloud API)
    if settings.groq_api_key:
        try:
            return GroqFilter()
        except Exception as e:
            logger.warning(f"Could not initialize Groq filter: {e}")

    # Try Ollama second (free and local)
    try:
        return OllamaFilter()
    except Exception as e:
        logger.warning(f"Could not initialize Ollama filter: {e}")

    # Fall back to OpenAI-compatible API if configured
    if settings.openai_api_key:
        try:
            return OpenAICompatibleFilter()
        except Exception as e:
            logger.warning(f"Could not initialize OpenAI filter: {e}")

    logger.error("No LLM filter available. Please configure Groq, Ollama, or OpenAI.")
    return None


def build_user_criteria() -> str:
    """Build a text description of user's job search criteria."""
    criteria = f"""
Job Search Criteria:
- Target Roles: {', '.join(settings.target_roles_list)}
- Remote Work: {'Required' if settings.remote_only else 'Preferred'}
- Company Size: Minimum {settings.min_employees} employees
- Company Age: Minimum {settings.min_years_in_business} years in business
- Company Type: {'Prefer public companies' if settings.prefer_public_companies else 'Public or private'}
- Job Level: Senior or above
- Industry: IT & Software, Data Engineering, Cloud/SaaS

Preferences:
- Strong preference for companies with stable growth and revenue
- Interest in cloud technologies, data platforms, and modern software architecture
- Looking for challenging technical roles with impact
"""
    return criteria
