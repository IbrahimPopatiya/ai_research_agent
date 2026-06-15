from sqlmodel import Session, select
from database.db import engine
from database.models import CommunityPost, AITool
from analysis.research_analyzer import run_analysis


def get_recent_news(limit=10):

    with Session(engine) as session:

        statement = select(CommunityPost)

        posts = session.exec(statement).all()

        return posts[:limit]

def get_recent_tools(limit=10):

    with Session(engine) as session:

        statement = select(AITool)

        tools = session.exec(statement).all()

        return tools[:limit]


def build_news_section():

    news = get_recent_news()

    section = "NEWS\n\n"

    for index, post in enumerate(news, start=1):

        section += f"{index}. {post.title}\n"
        section += f"{post.url}\n\n"

    return section

def build_tools_section():

    tools = get_recent_tools()

    section = "AI TOOLS\n\n"

    for tool in tools:

        section += f"Tool: {tool.name}\n"
        section += f"About: {tool.description}\n"
        section += f"Link: {tool.url}\n\n"

    return section


def build_research_section():

    analysis = run_analysis()

    section = "RESEARCH REPORT\n\n"

    section += analysis

    return section


def build_full_report():

    report = ""

    report += build_news_section()
    report += "\n----------------------\n\n"

    report += build_tools_section()
    report += "\n----------------------\n\n"

    report += build_research_section()

    return report