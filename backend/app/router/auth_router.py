from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repository.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.service.auth_service import AuthService

router = APIRouter()

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    id: str
    name: str
    email: str

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    repo = SQLAlchemyUserRepository(db)
    return AuthService(repo)

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, service: AuthService = Depends(get_auth_service)):
    user = service.authenticate_user(request.email, request.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email
    }

@router.get("/me")
async def read_users_me():
    # Placeholder for current user logic
    return {"user_id": "1", "email": "mock@example.com"}
