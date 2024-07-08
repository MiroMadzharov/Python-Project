# habit_tracker/app/tests/test_habits.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal, Base, engine
from app import models

@pytest.fixture(scope="module")
def test_db():
    """
    Fixture for creating a test database session.

    Yields:
        Session: Database session object
    """
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def client():
    """
    Fixture for creating a test client instance.

    Returns:
        TestClient: FastAPI test client
    """
    return TestClient(app)

def test_create_habit(client, test_db):
    """
    Test case for creating a habit.

    It verifies that a habit can be successfully created.

    Raises:
        AssertionError: If the expected response does not match the actual response
    """
    user_id = 1  # Assuming user with ID 1 exists in your test environment
    response = client.post(f"/habits/?user_id={user_id}", json={
        "name": "Test Habit",
        "description": "Test Description",
        "periodicity": "daily",
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Test Habit"

def test_read_habits(client, test_db):
    """
    Test case for reading habits.

    It verifies that habits for a specific user can be successfully retrieved.

    Raises:
        AssertionError: If the expected response does not match the actual response
    """
    response = client.get("/habits/?user_id=1")
    assert response.status_code == 200
    assert len(response.json()) > 0

def test_update_habit(client, test_db):
    """
    Test case for updating a habit.

    It verifies that a habit can be successfully updated.

    Raises:
        AssertionError: If the expected response does not match the actual response
    """
    habit_id = client.get("/habits/?user_id=1").json()[0]["id"]
    response = client.put(f"/habits/{habit_id}", json={
        "name": "Updated Habit",
        "description": "Updated Description",
        "periodicity": "weekly"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Habit"

def test_checkoff_habit(client, test_db):
    """
    Test case for checking off a habit.

    It verifies that a habit can be successfully checked off.

    Raises:
        AssertionError: If the expected response does not match the actual response
    """
    habit_id = client.get("/habits/?user_id=1").json()[0]["id"]
    response = client.put(f"/habits/{habit_id}/checkoff")
    assert response.status_code == 200
    assert response.json()["id"] == habit_id

def test_delete_habit(client, test_db):
    """
    Test case for deleting a habit.

    It verifies that a habit can be successfully deleted.

    Raises:
        AssertionError: If the expected response does not match the actual response
    """
    habit_id = client.get("/habits/?user_id=1").json()[0]["id"]
    response = client.delete(f"/habits/{habit_id}")
    assert response.status_code == 200
    assert response.json()["id"] == habit_id

def test_habit_streak(client, test_db):
    """
    Test case for getting habit streak.

    It verifies that the streak for a habit can be successfully retrieved.

    Raises:
        AssertionError: If the expected response does not match the actual response
    """
    habit_id = client.get("/habits/?user_id=1").json()[0]["id"]
    response = client.get(f"/habits/{habit_id}/streak/")
    assert response.status_code == 200
    assert isinstance(response.json(), int)

def test_habit_is_broken(client, test_db):
    """
    Test case for checking if a habit is broken.

    It verifies that the broken status of a habit can be successfully retrieved.

    Raises:
        AssertionError: If the expected response does not match the actual response
    """
    habit_id = client.get("/habits/?user_id=1").json()[0]["id"]
    response = client.get(f"/habits/{habit_id}/is_broken/")
    assert response.status_code == 200
    assert isinstance(response.json(), bool)
