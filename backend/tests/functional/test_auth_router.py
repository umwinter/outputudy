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


def test_register_success(client: TestClient, db_session: Session) -> None:
    response = client.post(
        "/api/auth/register",
        json={
            "name": "New User",
            "email": "new_user@example.com",
            "password": "newpassword123",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "new_user@example.com"
    assert data["name"] == "New User"
    assert "access_token" in data


def test_register_duplicate_email(client: TestClient, db_session: Session) -> None:
    # Setup existing user
    user = UserORM(
        name="Existing User",
        email="duplicate@example.com",
        hashed_password=get_password_hash("password"),
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/auth/register",
        json={
            "name": "New User",
            "email": "duplicate@example.com",
            "password": "newpassword123",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


def test_forgot_password_success(client: TestClient, db_session: Session) -> None:
    # Setup test user
    user = UserORM(
        name="Forgot User",
        email="forgot@example.com",
        hashed_password=get_password_hash("password"),
    )
    db_session.add(user)
    db_session.commit()

    response = client.post(
        "/api/auth/forgot-password",
        json={"email": "forgot@example.com"},
    )
    assert response.status_code == 200
    assert "receive a reset link" in response.json()["detail"]


def test_reset_password_success(client: TestClient, db_session: Session) -> None:
    # Setup test user
    user = UserORM(
        name="Reset User",
        email="reset@example.com",
        id=999,
        hashed_password=get_password_hash("oldpassword"),
    )
    db_session.add(user)
    db_session.commit()

    # Reset token is a JWT with type="password_reset" and sub=user_id.
    # We can use the security infrastructure or just mock/generate it.
    from datetime import timedelta

    from app.infrastructure.security import create_access_token

    token = create_access_token(
        data={"sub": "999", "type": "password_reset"},
        expires_delta=timedelta(minutes=15),
    )

    response = client.post(
        "/api/auth/reset-password",
        json={"token": token, "new_password": "newpassword456"},
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Password has been reset successfully."

    # Verify login with new password
    login_res = client.post(
        "/api/auth/login",
        json={"email": "reset@example.com", "password": "newpassword456"},
    )
    assert login_res.status_code == 200
