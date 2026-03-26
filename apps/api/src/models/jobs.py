from uuid import uuid4
from datetime import datetime, timezone
from pydantic import BaseModel
from pydantic.fields import Field
from .salary import SalaryRange


class JobCreator(BaseModel):
    title: str
    company: str | None = None
    location: str | None = None
    salary_range: SalaryRange | None = None
    created_at: datetime | None = None
    applied_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    description: str
    url: str | None = None


class Job(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    user_id: str
    title: str
    company: str | None = None
    location: str | None = None
    salary_range: SalaryRange | None = None
    created_at: datetime | None = None
    applied_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class JobDetailed(Job):
    description: str
    skills: str | None = None
    yoe: str | None = None
    benefits: str | None = None
    url: str | None = None


class JobConcise(Job):
    summary: str
    skills: str | None = None
    yoe: str | None = None


class JobList(BaseModel):
    total: int
    jobs: list[JobConcise]
