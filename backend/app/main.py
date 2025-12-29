from fastapi import FastAPI
from app.router import user_router

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from app.router import user_router
from app import auth

app.include_router(user_router.router, prefix="/api")
app.include_router(auth.router, prefix="/api/auth")

@app.get("/")
def read_root():
    return {"Hello": "World"}

