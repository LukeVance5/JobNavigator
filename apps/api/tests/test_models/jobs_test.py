import pytest
from pydantic import ValidationError
from src.models.jobs import Job, JobDetailed, JobConcise
from src.models.salary import SalaryRate, SalaryRange
from datetime import datetime


def test_create_job(sample_job: Job):
    """Tests basic job creation using the fixture."""
    assert sample_job.title == "Software Engineer"
    assert sample_job.company == "Tech Corp"
    assert sample_job.location == "San Francisco, CA"
    assert sample_job.user_id == "test_user_id"
    assert sample_job.salary_range is None


def test_job_default_values():
    """Tests that default values for id and applied_at are set."""
    job = Job(title="Data Scientist", company="Data Inc.", user_id="test_user_id")
    assert isinstance(job.id, str)
    assert len(job.id) > 0
    assert isinstance(job.applied_at, datetime)


def test_create_job_with_salary(sample_job_with_salary: Job):
    """Tests creating a job with a valid SalaryRange object."""
    assert sample_job_with_salary.title == "Senior Software Engineer"
    assert sample_job_with_salary.salary_range is not None
    assert sample_job_with_salary.salary_range.min == 120000


def test_create_job_with_invalid_salary_structure():
    """
    Tests that creating a job with a malformed salary dictionary
    raises a ValidationError. This confirms Pydantic's validation cascade.
    """
    with pytest.raises(ValidationError):
        Job(
            title="Product Manager",
            company="Innovate LLC",
            user_id="test_user_id",
            salary_range={"minimum": 100000, "maximum": 150000},  # wrong field names
        )


def test_create_job_detailed():
    """Tests creation of a JobDetailed instance."""
    job = JobDetailed(
        title="Backend Engineer",
        description="Developing server-side logic.",
        skills="Python, Django, PostgreSQL",
        user_id="test_user_id",
    )
    assert job.description == "Developing server-side logic."
    assert job.skills == "Python, Django, PostgreSQL"
    assert isinstance(job.id, str)


def test_create_job_concise():
    """Tests creation of a JobConcise instance."""
    job = JobConcise(
        title="Frontend Developer",
        summary="Building user interfaces.",
        skills="React, TypeScript, CSS",
        user_id="test_user_id",
    )
    assert job.summary == "Building user interfaces."
    assert job.skills == "React, TypeScript, CSS"
    assert isinstance(job.id, str)
