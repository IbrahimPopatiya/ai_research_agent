from sqlmodel import Session, select
from database.db import engine
from database.models import AITool
from database.models import CommunityPost


def save_ai_tool(tool_data):

    with Session(engine) as session:

        statement = select(AITool).where(AITool.url == tool_data["url"])
        existing_tool = session.exec(statement).first()

        if existing_tool:
            print("Tool already exists:", tool_data["name"])
            return

        tool = AITool(
            name=tool_data["name"],
            description=tool_data["description"],
            stars=tool_data["stars"],
            language=tool_data["language"],
            url=tool_data["url"]
        )

        session.add(tool)
        session.commit()

        print("Saved new tool:", tool_data["name"])




def save_community_post(post_data):

    with Session(engine) as session:

        statement = select(CommunityPost).where(
            CommunityPost.url == post_data["url"]
        )

        existing = session.exec(statement).first()

        if existing:
            print("Post already exists:", post_data["title"])
            return

        post = CommunityPost(
            title=post_data["title"],
            url=post_data["url"],
            score=post_data["score"],
            source=post_data["source"]
        )

        session.add(post)
        session.commit()

        print("Saved post:", post_data["title"])