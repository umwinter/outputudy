import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.orm_models import UserORM
from app.infrastructure.security import get_password_hash


@pytest.mark.asyncio
async def test_list_users(client: AsyncClient, db_session: AsyncSession) -> None:
    # Need to auth first
    import uuid

    from app.infrastructure.security import create_access_token

    # Create a user to auth with
    admin_id = uuid.uuid4()
    admin_user = UserORM(
        name="Admin",
        email="admin@example.com",
        id=admin_id,
        hashed_password=get_password_hash("pass"),
    )
    db_session.add(admin_user)

    # Setup test users
    user1 = UserORM(
        name="User1",
        email="user1@example.com",
        hashed_password=get_password_hash("pass"),
    )
    user2 = UserORM(
        name="User2",
        email="user2@example.com",
        hashed_password=get_password_hash("pass"),
    )
    db_session.add_all([user1, user2])
    await db_session.commit()

    token = create_access_token(data={"sub": str(admin_id)})
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get("/api/users", headers=headers)
    assert response.status_code == 200
    data = response.json()
    # Should see user1, user2, and admin
    assert len(data) >= 3
    emails = [u["email"] for u in data]
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails


@pytest.mark.asyncio
async def test_get_user_success(client: AsyncClient, db_session: AsyncSession) -> None:
    # Need to auth

    from app.infrastructure.security import create_access_token

    user = UserORM(
        name="Single User",
        email="single@example.com",
        hashed_password=get_password_hash("pass"),
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    token = create_access_token(data={"sub": str(user.id)})
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get(f"/api/users/{user.id}", headers=headers)
    assert response.status_code == 200
    assert response.json()["email"] == "single@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(
    client: AsyncClient, db_session: AsyncSession
) -> None:
    import uuid

    # Need to auth
    from app.infrastructure.security import create_access_token

    # Random ID for auth
    uid = uuid.uuid4()
    # Mock finding SOME user for auth? Or insert one?
    # Auth middleware fetches user from DB. So we MUST insert a user to auth with.
    user = UserORM(
        name="Auth User",
        email="auth_user@example.com",
        id=uid,
        hashed_password=get_password_hash("pass"),
    )
    db_session.add(user)
    await db_session.commit()

    token = create_access_token(data={"sub": str(uid)})
    headers = {"Authorization": f"Bearer {token}"}

    response = await client.get(f"/api/users/{uuid.uuid4()}", headers=headers)
    assert response.status_code == 200
    assert response.json() is None
