from fastapi.testclient import TestClient
from models.user import User
from src.models.jobs import Job, JobCreator, JobDetailed, JobConcise, JobList
import json
from tests.conftest import junior_job_creator
from unittest.mock import MagicMock
from pathlib import Path


def test_create_and_read_job(
    client: TestClient,
    test_user,
):
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    login_response = response.json()
    token = login_response["access_token"]
    user_id = login_response["user_id"]
    headers = {"Authorization": f"Bearer {token}"}

    junior_job = job_loader("junior_python_engineer.json", user_id)
    job_payload = json.loads(junior_job.model_dump_json())
    response = client.post("/api/v1/jobs/", json=job_payload, headers=headers)
    assert response.status_code == 200
    created_job = Job(**response.json())
    assert created_job.title == job_payload["title"]
    assert created_job.id is not None

    # Read the job
    job_id = created_job.id
    response = client.get(f"/api/v1/jobs/{job_id}", headers=headers)
    assert response.status_code == 200
    read_job = JobDetailed(**response.json())
    assert read_job.title == job_payload["title"]
    assert read_job.id == job_id


def test_multiple_jobs(client: TestClient, test_user):
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    login_response = response.json()
    token = login_response["access_token"]
    user_id = login_response["user_id"]
    headers = {"Authorization": f"Bearer {token}"}

    junior_job = job_loader("junior_python_engineer.json", user_id)
    job_payload = json.loads(junior_job.model_dump_json())
    response = client.post("/api/v1/jobs/", json=job_payload, headers=headers)
    assert response.status_code == 200
    intermediate_job = job_loader("intermediate_ruby_developer.json", user_id)
    job_payload = json.loads(intermediate_job.model_dump_json())
    response = client.post("/api/v1/jobs/", json=job_payload, headers=headers)
    assert response.status_code == 200
    junior_job = job_loader("intermediate_ruby_developer.json", user_id)
    job_payload = json.loads(junior_job.model_dump_json())
    response = client.post("/api/v1/jobs/", json=job_payload, headers=headers)
    assert response.status_code == 200
    response = client.get("/api/v1/jobs/", headers=headers)
    assert response.status_code == 200
    jobs = JobList(**response.json())
    assert len(jobs.jobs) == 3


def job_loader(name: str, user_id: str) -> JobCreator:
    path = Path(__file__).resolve().parent.parent / "mocks" / name
    job = {}
    with open(path, "r") as f:
        job = json.load(f)
    if isinstance(job.get("description"), list):
        job["description"] = "\n".join(job["description"])
    return JobCreator(**job)


def test_delete_job(
    client: TestClient,
    test_user,
):
    login_data = {
        "username": test_user["email"],
        "password": test_user["password"],
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    login_response = response.json()
    token = login_response["access_token"]
    user_id = login_response["user_id"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a job to delete
    junior_job = job_loader("junior_python_engineer.json", user_id)
    job_payload = json.loads(junior_job.model_dump_json())
    response = client.post("/api/v1/jobs/", json=job_payload, headers=headers)
    assert response.status_code == 200
    created_job = Job(**response.json())
    job_id = created_job.id

    # Test successful deletion
    response = client.delete(f"/api/v1/jobs/{job_id}", headers=headers)
    assert response.status_code == 200
    deleted_job = Job(**response.json())
    assert deleted_job.id == job_id

    # Test job is no longer found
    response = client.get(f"/api/v1/jobs/{job_id}", headers=headers)
    assert response.status_code == 404

    # Test deleting a non-existent job
    response = client.delete("/api/v1/jobs/non_existent_id", headers=headers)
    assert response.status_code == 404

    # Test unauthorized deletion (no token)
    response = client.delete(f"/api/v1/jobs/{job_id}")
    assert response.status_code == 401
