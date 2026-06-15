from sqlmodel import create_engine,SQLModel
from database import models
DATABASE_URL = "sqlite:///./ai_research.db"

engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)