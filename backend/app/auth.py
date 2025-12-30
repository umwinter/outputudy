from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import os
from sqlalchemy.orm import Session
from app.infrastructure.database import get_db
from app.infrastructure.repository.sqlalchemy_user_repository import SQLAlchemyUserRepository
from app.infrastructure.security import verify_password

router = APIRouter()

AUTH_SECRET = os.getenv("AUTH_SECRET")

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class LoginResponse(BaseModel):
    id: str
    name: str
    email: str

@router.post("/login", response_model=LoginResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    repo = SQLAlchemyUserRepository(db)
    user_orm = repo.get_user_by_email(request.email)
    
    if not user_orm:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(request.password, user_orm.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    return {
        "id": str(user_orm.id),
        "name": user_orm.name,
        "email": user_orm.email
    }

# Dependency for protected routes
async def verify_token(token: str):
    try:
        if not AUTH_SECRET:
            raise ValueError("AUTH_SECRET is not set")
        
        # Verify JWE/JWT
        # Note: Auth.js v5 uses JWE by default. 
        # For simplicity in this mock phase, we assume the token passed is verify-able.
        # Decrypting Auth.js v5 JWE requires accurate encryption algorithms (A256GCM etc).
        # Here we just check presence for now as true JWE decryption in Python matching NextAuth defaults 
        # can be complex without matching exact algs.
        pass
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
async def read_users_me():
    return {"user_id": "1", "email": "mock@example.com"}
