from typing import Optional
from app.domain.models import User
from app.domain.repository import UserRepository
from app.infrastructure.security import verify_password

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = self.user_repo.get_user_by_email(email)
        if not user:
            return None
        
        if not user.hashed_password:
            return None

        if not verify_password(password, user.hashed_password):
            return None
            
        return user
