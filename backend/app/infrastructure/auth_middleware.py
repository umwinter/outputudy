from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.domain.models import User
from app.infrastructure.database import get_db
from app.infrastructure.repository.sqlalchemy_user_repository import (
    SQLAlchemyUserRepository,
)
from app.infrastructure.security import verify_access_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    repo = SQLAlchemyUserRepository(db)
    user = repo.get_user_by_id(int(user_id))
    if user is None:
        raise credentials_exception

    return user
