from sqlalchemy.orm import Session

from app.domain.models import User
from app.domain.repository import UserRepository
from app.infrastructure.orm_models import UserORM


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_user_by_id(self, user_id: int) -> User | None:
        user_orm = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        if user_orm:
            return User.model_validate(user_orm)
        return None

    def get_user_by_email(self, email: str) -> User | None:
        user_orm = self.db.query(UserORM).filter(UserORM.email == email).first()
        if user_orm:
            return User.model_validate(user_orm)
        return None

    def list_users(self) -> list[User]:
        users_orm = self.db.query(UserORM).all()
        return [User.model_validate(u) for u in users_orm]

    def create_user(self, name: str, email: str, hashed_password: str) -> User:
        user_orm = UserORM(name=name, email=email, hashed_password=hashed_password)
        self.db.add(user_orm)
        self.db.commit()
        self.db.refresh(user_orm)
        return User.model_validate(user_orm)

    def update_user_password(self, user_id: int, hashed_password: str) -> None:
        self.db.query(UserORM).filter(UserORM.id == user_id).update(
            {"hashed_password": hashed_password}
        )
        self.db.commit()
