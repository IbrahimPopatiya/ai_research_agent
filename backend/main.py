from fastapi import FastAPI
from backend.config import settings
from database.db import engine
from sqlmodel import SQLModel

app = FastAPI(
    title="AI Research Intelligence System"
)

@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def root():
    return {
        "message": "AI Research Agent Running",
        "database": settings.DATABASE_URL
    }