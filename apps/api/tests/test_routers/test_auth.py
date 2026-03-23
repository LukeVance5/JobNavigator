from fastapi.testclient import TestClient
from src.models.user import User, UserCreate
from src.models.jobs import JobCreator
import json
from unittest.mock import MagicMock


def test_register_user(client: TestClient):
    # Test that a new user can be created successfully
    user_payload = {"email": "test@example.com", "password": "testpassword"}
    response = client.post("/api/v1/auth/register", json=user_payload)
    assert response.status_code == 200
    created_user = User(**response.json())
    assert created_user.email == user_payload["email"]
    assert created_user.id is not None

    # Test that a user cannot be created with an existing email
    response = client.post("/api/v1/auth/register", json=user_payload)
    assert response.status_code == 400


def test_login_for_access_token(client: TestClient):
    # Test that a registered user can log in and get a JWT token
    user_payload = {"email": "test2@example.com", "password": "testpassword"}
    client.post("/api/v1/auth/register", json=user_payload)

    login_payload = {"username": "test2@example.com", "password": "testpassword"}
    response = client.post("/api/v1/auth/login", data=login_payload)
    assert response.status_code == 200
    token = response.json()
    assert "access_token" in token
    assert token["token_type"] == "bearer"

    # Test that a user cannot log in with an incorrect password
    login_payload["password"] = "wrongpassword"
    response = client.post("/api/v1/auth/login", data=login_payload)
    assert response.status_code == 401

    # Test that a non-existent user cannot log in
    login_payload["username"] = "nosuchuser@example.com"
    response = client.post("/api/v1/auth/login", data=login_payload)
    assert response.status_code == 401


def test_protected_job_endpoints(client: TestClient, junior_job_creator: JobCreator):
    # Create a user and get a token
    user_payload = {"email": "owner@example.com", "password": "testpassword"}
    client.post("/api/v1/auth/register", json=user_payload)
    login_payload = {"username": "owner@example.com", "password": "testpassword"}
    response = client.post("/api/v1/auth/login", data=login_payload)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test that the POST /jobs/ endpoint is protected
    job_payload = json.loads(junior_job_creator.model_dump_json())
    response = client.post("/api/v1/jobs/", json=job_payload)
    assert response.status_code == 401  # No token provided

    response = client.post("/api/v1/jobs/", json=job_payload, headers=headers)
    assert response.status_code == 200
    created_job_id = response.json()["id"]

    # Test that the GET /jobs/{job_id} endpoint is protected
    response = client.get(f"/api/v1/jobs/{created_job_id}")
    assert response.status_code == 401  # No token provided

    response = client.get(f"/api/v1/jobs/{created_job_id}", headers=headers)
    assert response.status_code == 200

    # Create a second user and get a token
    user_payload_2 = {"email": "notowner@example.com", "password": "testpassword"}
    client.post("/api/v1/auth/register", json=user_payload_2)
    login_payload_2 = {"username": "notowner@example.com", "password": "testpassword"}
    response = client.post("/api/v1/auth/login", data=login_payload_2)
    token_2 = response.json()["access_token"]
    headers_2 = {"Authorization": f"Bearer {token_2}"}

    # Test that the second user cannot access the job
    response = client.get(f"/api/v1/jobs/{created_job_id}", headers=headers_2)
    assert response.status_code == 404
