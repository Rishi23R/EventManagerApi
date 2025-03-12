import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#  Create a test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#  Override the database dependency for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

#  Create a test client
client = TestClient(app)

#  Setup the test database
@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

#  Test Attendee Registration
def test_register_attendee():
    response = client.post("/attendees/", json={"name": "John Doe", "email": "john@example.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"

#  Test Attendee Check-in
def test_check_in_attendee():
    response = client.put("/check-in/1")
    assert response.status_code == 200 or response.status_code == 400  # If already checked in

#  Test API Behavior for Invalid Attendee ID
def test_check_in_invalid_attendee():
    response = client.put("/check-in/999")  # Non-existent ID
    assert response.status_code == 404
    assert response.json()["detail"] == "Attendee not found"
