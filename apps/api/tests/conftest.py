import pytest
import json
from pathlib import Path
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool


from main import app
from database import Base, get_db
from routers.jobs import get_ai_service
from models.jobs import Job, JobCreator
from models.salary import SalaryRate, SalaryRange
from models.database_models import JobModel

# Use StaticPool to keep the in-memory connection alive for the duration of the test
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Provides a fresh database for every test."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_ai_service():
    """Creates a mock of CareerAIService to avoid real Vertex AI calls."""
    mock = MagicMock()
    mock.summarize_job.return_value = "This is a mocked summary for testing."
    return mock


@pytest.fixture
def client(db_session, mock_ai_service):
    """Configures the TestClient with dependency overrides."""
    # Override the DB dependency
    app.dependency_overrides[get_db] = lambda: db_session
    # Override the AI service dependency
    app.dependency_overrides[get_ai_service] = lambda: mock_ai_service

    with TestClient(app) as c:
        yield c

    # Always clear overrides after the test to prevent side effects
    app.dependency_overrides.clear()


# --- Data Fixtures ---


@pytest.fixture
def sample_job():
    return Job(
        title="Software Engineer",
        company="Tech Corp",
        location="San Francisco, CA",
        user_id="test_user_id",
    )


@pytest.fixture
def sample_job_with_salary():
    return Job(
        title="Senior Software Engineer",
        company="Innovate LLC",
        location="New York, NY",
        user_id="test_user_id",
        salary_range=SalaryRange(
            min=120000,
            max=180000,
            currency="USD",
            rate=SalaryRate.YEARLY,
        ),
    )


@pytest.fixture
def sample_job_json():
    path = Path(__file__).parent / "mocks" / "junior_python_engineer.json"
    with open(path, "r") as f:
        return json.load(f)


@pytest.fixture
def test_user(client: TestClient):
    """Creates a new user and returns the user's details."""
    user_data = {
        "email": "test@example.com",
        "password": "testpassword",
    }
    response = client.post("/api/v1/auth/register", json=user_data)
    # if the user already exists, we can ignore the error
    # and proceed to login.
    if response.status_code == 400 and "Email already registered" in response.text:
        pass
    else:
        assert response.status_code == 200
    return user_data


@pytest.fixture
def junior_job_creator(sample_job_json):
    data = sample_job_json.copy()
    if isinstance(data.get("description"), list):
        data["description"] = "\n".join(data["description"])
    data["user_id"] = "user_12345"
    return JobCreator(**data)
