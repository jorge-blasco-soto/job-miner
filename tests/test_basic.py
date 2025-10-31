"""Simple tests to verify the system works."""
import pytest

from jobminer.companies import (get_companies, get_company_info,
                                is_established_company)
from jobminer.config import settings
from jobminer.models import Company, Job


def test_company_database():
    """Test company database has entries."""
    companies = get_companies()
    assert len(companies) > 0
    assert all(isinstance(c, Company) for c in companies)


def test_company_criteria():
    """Test companies meet criteria."""
    companies = get_companies()

    for company in companies:
        # Check employee count if specified
        if company.employee_count:
            assert company.employee_count >= 200, f"{company.name} has less than 200 employees"

        # Check years in business if specified
        if company.founded_year:
            years = 2024 - company.founded_year
            assert years >= 5, f"{company.name} has been in business less than 5 years"


def test_is_established_company():
    """Test company lookup function."""
    assert is_established_company("Snowflake")
    assert is_established_company("snowflake")  # Case insensitive
    assert is_established_company("Microsoft")
    assert not is_established_company("NonExistentCompany")


def test_get_company_info():
    """Test getting company details."""
    company = get_company_info("Snowflake")
    assert company is not None
    assert company.name == "Snowflake"
    assert company.employee_count is not None

    # Non-existent company
    assert get_company_info("NonExistent") is None


def test_job_model():
    """Test Job model creation."""
    job = Job(
        title="Senior Data Engineer",
        company="Snowflake",
        url="https://example.com/job",
        location="Remote",
        is_remote=True
    )

    assert job.title == "Senior Data Engineer"
    assert job.is_remote is True
    assert job.id is not None


def test_settings():
    """Test settings load correctly."""
    assert settings.min_employees >= 0
    assert settings.min_years_in_business >= 0
    assert len(settings.target_roles_list) > 0


def test_target_roles():
    """Test target roles are configured."""
    roles = settings.target_roles_list
    assert len(roles) > 0

    expected_roles = [
        "data engineer",
        "senior data engineer",
        "software engineer",
        "solutions architect"
    ]

    for expected in expected_roles:
        assert any(expected.lower() in role.lower() for role in roles), \
            f"Expected role '{expected}' not found in target roles"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
