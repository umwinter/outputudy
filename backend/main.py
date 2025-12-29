from fastapi import FastAPI
from backend.app.router import user_router

app = FastAPI()

app.include_router(user_router.router, prefix="/api")

@app.get("/")
def read_root():
    return {"Hello": "World"}
    return {"Hello": "World"}
