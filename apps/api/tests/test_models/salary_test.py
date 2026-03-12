import pytest
from pydantic import ValidationError
from src.models.salary import SalaryRate, SalaryRange


def test_create_salary_range():
    salary = SalaryRange(min=50000, max=70000, currency="USD", rate=SalaryRate.YEARLY)
    assert salary.min == 50000
    assert salary.max == 70000
    assert salary.currency == "USD"
    assert salary.rate == SalaryRate.YEARLY


def test_salary_range_invalid_range():
    with pytest.raises(ValidationError):
        SalaryRange(min=80000, max=70000, currency="USD", rate=SalaryRate.YEARLY)


@pytest.mark.parametrize(
    "rate_input, expected_rate",
    [
        ("hourly", SalaryRate.HOURLY),
        ("hr", SalaryRate.HOURLY),
        ("monthly", SalaryRate.MONTHLY),
        ("mo", SalaryRate.MONTHLY),
        ("yearly", SalaryRate.YEARLY),
        ("yr", SalaryRate.YEARLY),
        ("annually", SalaryRate.YEARLY),
        ("annum", SalaryRate.YEARLY),
    ],
)
def test_salary_rate_validation(rate_input, expected_rate):
    salary = SalaryRange(min=50000, max=70000, currency="USD", rate=rate_input)
    assert salary.rate == expected_rate


def test_job_with_salary(sample_job_with_salary):
    assert sample_job_with_salary.salary_range is not None
    assert sample_job_with_salary.salary_range.min == 120000
    assert sample_job_with_salary.salary_range.max == 180000
    assert sample_job_with_salary.salary_range.rate == SalaryRate.YEARLY


def test_job_without_salary(sample_job):
    assert sample_job.salary_range is None
