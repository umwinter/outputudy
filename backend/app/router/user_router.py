from fastapi import APIRouter, Depends
from typing import List
from backend.app.usecase.user_usecase import UserUsecase
from backend.app.infrastructure.repository.user_repository import InMemoryUserRepository
from backend.app.domain.models import User

router = APIRouter()

# Dependency Injection (Manual for now, typically handled by DI framework or FastAPI Depends)
def get_user_usecase() -> UserUsecase:
    # In a real app, this would get the repository from DB connection
    repo = InMemoryUserRepository()
    return UserUsecase(repo)

@router.get("/users", response_model=List[User])
def list_users(usecase: UserUsecase = Depends(get_user_usecase)):
    return usecase.get_users()

@router.get("/users/{user_id}", response_model=User | None)
def get_user(user_id: int, usecase: UserUsecase = Depends(get_user_usecase)):
    return usecase.get_user_by_id(user_id)
