from sqlmodel import SQLModel, Field
from typing import Optional

class News(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    source: str
    link: str
    summary: Optional[str] = None



class AITool(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str]
    stars: int
    language: Optional[str]
    url: str



class CommunityPost(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True)

    title: str
    source: str
    url: str
    score: Optional[int] = None