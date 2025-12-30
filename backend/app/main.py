from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.router import auth_router, user_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/auth", tags=["auth"])
app.include_router(user_router.router, prefix="/api", tags=["users"])


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}
