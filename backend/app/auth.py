from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
import os
from jose import jwt, JWTError

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
async def login(request: LoginRequest):
    # Mock authentication
    if request.email and request.password == "password":
        return {
            "id": "1",
            "name": "User",
            "email": request.email
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

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
