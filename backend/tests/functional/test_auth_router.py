import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.orm_models import UserORM
from app.infrastructure.security import get_password_hash


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient, db_session: AsyncSession) -> None:
    # Setup test user
    password = "testpassword"
    user = UserORM(
        name="Test User",
        email="test_router@example.com",
        hashed_password=get_password_hash(password),
    )
    db_session.add(user)
    await db_session.commit()

    # Test login
    response = await client.post(
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


@pytest.mark.asyncio
async def test_login_wrong_password(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    # Setup test user
    password = "testpassword"
    user = UserORM(
        name="Test User",
        email="wrong_pass@example.com",
        hashed_password=get_password_hash(password),
    )
    db_session.add(user)
    await db_session.commit()

    # Test login with wrong password
    response = await client.post(
        "/api/auth/login",
        json={"email": "wrong_pass@example.com", "password": "incorrect_password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient) -> None:
    response = await client.post(
        "/api/auth/login",
        json={"email": "nonexistent@example.com", "password": "any_password"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


@pytest.mark.asyncio
async def test_read_users_me_success(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    # Setup test user
    password = "testpassword"
    user = UserORM(
        name="Auth User",
        email="auth_me@example.com",
        hashed_password=get_password_hash(password),
    )
    db_session.add(user)
    await db_session.commit()

    # 1. Login to get token
    login_res = await client.post(
        "/api/auth/login",
        json={"email": "auth_me@example.com", "password": password},
    )
    token = login_res.json()["access_token"]

    # 2. Access /me with token
    response = await client.get(
        "/api/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "auth_me@example.com"
    assert data["name"] == "Auth User"


@pytest.mark.asyncio
async def test_read_users_me_unauthorized(client: AsyncClient) -> None:
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient, db_session: AsyncSession) -> None:
    response = await client.post(
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


@pytest.mark.asyncio
async def test_register_duplicate_email(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    # Setup existing user
    user = UserORM(
        name="Existing User",
        email="duplicate@example.com",
        hashed_password=get_password_hash("password"),
    )
    db_session.add(user)
    await db_session.commit()

    response = await client.post(
        "/api/auth/register",
        json={
            "name": "New User",
            "email": "duplicate@example.com",
            "password": "newpassword123",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


@pytest.mark.asyncio
async def test_forgot_password_success(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    # Setup test user
    user = UserORM(
        name="Forgot User",
        email="forgot@example.com",
        hashed_password=get_password_hash("password"),
    )
    db_session.add(user)
    await db_session.commit()

    response = await client.post(
        "/api/auth/forgot-password",
        json={"email": "forgot@example.com"},
    )
    assert response.status_code == 200
    assert "receive a reset link" in response.json()["detail"]


@pytest.mark.asyncio
async def test_reset_password_success(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    import uuid
    from datetime import timedelta

    from app.infrastructure.security import create_access_token

    user_id = uuid.uuid4()
    # Setup test user
    user = UserORM(
        name="Reset User",
        email="reset@example.com",
        id=user_id,
        hashed_password=get_password_hash("oldpassword"),
    )
    db_session.add(user)
    await db_session.commit()

    # Reset token is a JWT with type="password_reset" and sub=user_id.
    token = create_access_token(
        data={"sub": str(user_id), "type": "password_reset"},
        expires_delta=timedelta(minutes=15),
    )

    response = await client.post(
        "/api/auth/reset-password",
        json={"token": token, "new_password": "newpassword456"},
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Password has been reset successfully."

    # Verify login with new password
    login_res = await client.post(
        "/api/auth/login",
        json={"email": "reset@example.com", "password": "newpassword456"},
    )
    assert login_res.status_code == 200
