# habit_tracker/app/tests/test_auth.py

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    """
    Test case for user creation endpoint (/auth/signup/).

    It verifies that a user can be successfully created.

    Raises:
        AssertionError: If the expected response does not match the actual response
    """
    response = client.post(
        "/auth/signup/",
        json={"first_name": "John", "last_name": "Doe",
              "email": "john@example.com", "password": "password"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "john@example.com"


def test_login_user():
    """
    Test case for user login endpoint (/auth/login/).

    It verifies that a user can successfully log in with correct credentials.

    Raises:
        AssertionError: If the expected response does not match the actual response
    """
    response = client.get(
        "/auth/login/?email=john@example.com&password=password")
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}
