from unittest.mock import AsyncMock, MagicMock

import pytest

from app.domain.models import User
from app.domain.repository import UserRepository
from app.infrastructure.security import get_password_hash
from app.service.auth_service import AuthService


@pytest.mark.asyncio
async def test_authenticate_user_success() -> None:
    # Arrange
    mock_repo = MagicMock(spec=UserRepository)
    password = "correct_password"
    hashed = get_password_hash(password)
    mock_user = User(
        id=1, name="Test User", email="test@example.com", hashed_password=hashed
    )
    mock_repo.get_user_by_email = AsyncMock(return_value=mock_user)

    service = AuthService(mock_repo)

    # Act
    authenticated_user = await service.authenticate_user("test@example.com", password)

    # Assert
    assert authenticated_user is not None
    assert authenticated_user.email == "test@example.com"
    mock_repo.get_user_by_email.assert_called_once_with("test@example.com")


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password() -> None:
    # Arrange
    mock_repo = MagicMock(spec=UserRepository)
    hashed = get_password_hash("correct_password")
    mock_user = User(
        id=1, name="Test User", email="test@example.com", hashed_password=hashed
    )
    mock_repo.get_user_by_email = AsyncMock(return_value=mock_user)

    service = AuthService(mock_repo)

    # Act
    authenticated_user = await service.authenticate_user(
        "test@example.com", "wrong_password"
    )

    # Assert
    assert authenticated_user is None


@pytest.mark.asyncio
async def test_authenticate_user_not_found() -> None:
    # Arrange
    mock_repo = MagicMock(spec=UserRepository)
    mock_repo.get_user_by_email = AsyncMock(return_value=None)

    service = AuthService(mock_repo)

    # Act
    authenticated_user = await service.authenticate_user(
        "nonexistent@example.com", "any_password"
    )

    # Assert
    assert authenticated_user is None
