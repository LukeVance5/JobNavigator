from fastapi.testclient import TestClient
from src.models.jobs import Job, JobCreator, JobDetailed
import json
from tests.conftest import junior_job_creator
from unittest.mock import MagicMock


def test_create_and_read_job(
    client: TestClient,
    junior_job_creator: JobCreator,
):
    # Create a job
    job_payload = json.loads(junior_job_creator.model_dump_json())
    response = client.post("/api/v1/jobs/", json=job_payload)
    assert response.status_code == 200
    created_job = Job(**response.json())
    assert created_job.title == job_payload["title"]
    assert created_job.id is not None

    # Read the job
    job_id = created_job.id
    response = client.get(f"/api/v1/jobs/{job_id}")
    assert response.status_code == 200
    read_job = JobDetailed(**response.json())
    assert read_job.title == job_payload["title"]
    assert read_job.id == job_id
