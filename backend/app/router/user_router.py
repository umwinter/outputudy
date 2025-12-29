from fastapi import APIRouter, Depends
from typing import List
from app.service.user_service import UserService
from app.infrastructure.repository.user_repository import InMemoryUserRepository
from app.domain.models import User

router = APIRouter()

# Dependency Injection (Manual for now, typically handled by DI framework or FastAPI Depends)
def get_user_service() -> UserService:
    # In a real app, this would get the repository from DB connection
    repo = InMemoryUserRepository()
    return UserService(repo)

@router.get("/users", response_model=List[User])
def list_users(service: UserService = Depends(get_user_service)):
    return service.get_users()

@router.get("/users/{user_id}", response_model=User | None)
def get_user(user_id: int, service: UserService = Depends(get_user_service)):
    return service.get_user_by_id(user_id)
