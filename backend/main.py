from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from backend.config import settings
from backend.routes import router
from database.db import engine
from sqlmodel import SQLModel
import os

app = FastAPI(
    title="AI Research Intelligence System"
)

app.include_router(router)

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.on_event("startup")
def on_startup():
    SQLModel.metadata.create_all(engine)


@app.get("/")
def root():
    return FileResponse(os.path.join(frontend_dir, "index.html"))