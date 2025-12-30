from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.infrastructure.orm_models import UserORM
from app.infrastructure.security import get_password_hash


def test_login_success(client: TestClient, db_session: Session) -> None:
    # Setup test user
    password = "testpassword"
    user = UserORM(
        name="Test User",
        email="test_router@example.com",
        hashed_password=get_password_hash(password),
    )
    db_session.add(user)
    db_session.commit()

    # Test login
    response = client.post(
        "/api/auth/login",
        json={"email": "test_router@example.com", "password": password},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test_router@example.com"
    assert "id" in data
    assert data["name"] == "Test User"
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client: TestClient, db_session: Session) -> None:
    # Setup test user
    password = "testpassword"
    user = UserORM(
        name="Test User",
        email="wrong_pass@example.com",
        hashed_password=get_password_hash(password),
    )
    db_session.add(user)
    db_session.commit()

    # Test login with wrong password
    response = client.post(
        "/api/auth/login",
        json={"email": "wrong_pass@example.com", "password": "incorrect_password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_login_nonexistent_user(client: TestClient) -> None:
    response = client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "any_password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


def test_read_users_me_success(client: TestClient, db_session: Session) -> None:
    # Setup test user
    password = "testpassword"
    user = UserORM(
        name="Auth User",
        email="auth_me@example.com",
        hashed_password=get_password_hash(password),
    )
    db_session.add(user)
    db_session.commit()

    # 1. Login to get token
    login_res = client.post(
        "/api/auth/login",
        json={"email": "auth_me@example.com", "password": password},
    )
    token = login_res.json()["access_token"]

    # 2. Access /me with token
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "auth_me@example.com"
    assert data["name"] == "Auth User"


def test_read_users_me_unauthorized(client: TestClient) -> None:
    response = client.get("/api/auth/me")
    assert response.status_code == 401
