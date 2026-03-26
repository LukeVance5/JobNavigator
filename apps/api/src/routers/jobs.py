import os
from uuid import uuid4
from dotenv import load_dotenv

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from database import get_db
from core.security import get_current_user
from models.database_models import JobModel, UserModel
from models.jobs import Job, JobDetailed, JobCreator, JobList
from services.CareerAIService import CareerAIService

load_dotenv()


router = APIRouter()


# Initialize the AI Client here
_ai_service_instance = None


def get_ai_service():
    global _ai_service_instance
    if _ai_service_instance is None:
        project_id = os.getenv("GOOGLE_PROJECT_ID")
        if project_id is None:
            raise ValueError("GOOGLE_PROJECT_ID environment variable not set")
        # Initialize with Vertex settings
        _ai_service_instance = CareerAIService(project_id=project_id)
    return _ai_service_instance


@router.post("/", response_model=Job)
def create_job(
    job: JobCreator,
    db: Session = Depends(get_db),
    ai_service: CareerAIService = Depends(get_ai_service),  # Injected!
    current_user: UserModel = Depends(get_current_user),
):
    # 1. Let the service handle the AI heavy lifting
    summary = ai_service.summarize_job(job.description)

    # 2. Process your data (Business Logic)
    job_data = job.model_dump(exclude={"salary_range"})
    if job.salary_range:
        job_data["min_salary"] = job.salary_range.min
        job_data["max_salary"] = job.salary_range.max
        job_data["currency"] = job.salary_range.currency
        job_data["rate"] = job.salary_range.rate.value

    job_data["summary"] = summary
    job_data["id"] = str(uuid4())
    job_data["user_id"] = current_user.id

    # 3. Save to Database
    db_job = JobModel(**job_data)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


@router.get("/{job_id}", response_model=JobDetailed)
def read_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_job = (
        db.query(JobModel)
        .filter(JobModel.id == job_id, JobModel.user_id == current_user.id)
        .first()
    )
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return db_job


@router.delete("/{job_id}", response_model=Job)
def delete_job(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
):
    db_job = (
        db.query(JobModel)
        .filter(JobModel.id == job_id, JobModel.user_id == current_user.id)
        .first()
    )
    if db_job is None:
        raise HTTPException(status_code=404, detail="Job not found")

    db.delete(db_job)
    db.commit()
    return db_job


@router.get("/", response_model=JobList)
def read_user_jobs(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user),
    skip: int = 0,
    limit: int = Query(default=100, lte=1000),
):
    """
    Retrieves a paginated list of jobs for the currently authenticated user,
    sorted by application date (oldest first).
    """
    base_query = db.query(JobModel).filter(JobModel.user_id == current_user.id)

    total_count = base_query.count()

    user_jobs = (
        base_query.order_by(
            JobModel.applied_at.asc()
        )  # Sort by oldest application first
        .offset(skip)
        .limit(limit)
        .all()
    )
    return {"total": total_count, "jobs": user_jobs}
