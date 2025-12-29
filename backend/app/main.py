from fastapi import FastAPI
from app.router import user_router

app = FastAPI()

app.include_router(user_router.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}

