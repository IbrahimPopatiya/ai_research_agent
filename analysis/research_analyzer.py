import os
from openai import OpenAI
from backend.config import settings
from sqlmodel import Session, select
from database.db import engine
from database.models import CommunityPost

client = OpenAI(api_key=settings.OPENAI_API_KEY)

def analyze_text(content):

    prompt = f"""
You are an AI research analyst.

Analyze the following text and extract:

1. Summary
2. AI tools mentioned
3. Important insights

Text:
{content}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content




def get_recent_posts():

    with Session(engine) as session:

        statement = select(CommunityPost)

        posts = session.exec(statement).all()

        return posts


def run_analysis():

    posts = get_recent_posts()

    combined_text = ""

    for post in posts:
        combined_text += post.title + "\n"

    report = analyze_text(combined_text)

    return report
