import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.orm_models import UserORM
from app.infrastructure.security import get_password_hash


@pytest.mark.asyncio
async def test_list_users(client: TestClient, db_session: AsyncSession) -> None:
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

    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    emails = [u["email"] for u in data]
    assert "user1@example.com" in emails
    assert "user2@example.com" in emails


@pytest.mark.asyncio
async def test_get_user_success(client: TestClient, db_session: AsyncSession) -> None:
    user = UserORM(
        name="Single User",
        email="single@example.com",
        hashed_password=get_password_hash("pass"),
    )
    db_session.add(user)
    await db_session.commit()

    # Reuse the ID from the commited user
    # Note: UserORM ID autoincrement might need explicit fetch or refresh
    # if not returning but object identity map persists?
    # Better to fetch user by email or refresh
    await db_session.refresh(user)

    response = client.get(f"/api/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["email"] == "single@example.com"


@pytest.mark.asyncio
async def test_get_user_not_found(client: TestClient) -> None:
    response = client.get("/api/users/99999")
    # For now it returns null or 404?
    # Router says: return service.get_user_by_id(user_id) which returns User | None
    # FastAPI returns null (200) if no 404 raised?
    # Actually user_router.py simply returns the user. If None, it returns null.
    # It might be better to 404, but current implementation expects what?
    # Previous tests expected what?
    # Let's check user_router.py code.
    # It returns "User | None".
    # So response.json() is null.
    assert response.status_code == 200
    assert response.json() is None
