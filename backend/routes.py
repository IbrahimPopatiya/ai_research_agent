from fastapi import APIRouter, HTTPException
from sqlmodel import Session, select
from database.db import engine
from database.models import AITool, CommunityPost, News
from collectors.github_collector import collect_and_store_ai_tools, collect_ai_tools
from collectors.hackernews_collector import collect_hn_ai_posts
from collectors.reddit_json_collector import collect_reddit_ai_posts
from database.crud import save_ai_tool, save_community_post
from reports.report_builder import build_full_report, build_news_section, build_tools_section

router = APIRouter(prefix="/api")


@router.get("/tools")
def get_tools():
    with Session(engine) as session:
        tools = session.exec(select(AITool)).all()
        return tools


@router.get("/posts")
def get_posts():
    with Session(engine) as session:
        posts = session.exec(select(CommunityPost)).all()
        return posts


@router.get("/news")
def get_news():
    with Session(engine) as session:
        news = session.exec(select(News)).all()
        return news


@router.post("/collect/github")
def collect_github():
    try:
        tools = collect_ai_tools()
        saved = 0
        for tool in tools:
            save_ai_tool(tool)
            saved += 1
        return {"message": f"GitHub collection complete", "discovered": len(tools)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/collect/hackernews")
def collect_hackernews():
    try:
        posts = collect_hn_ai_posts()
        for post in posts:
            save_community_post(post)
        return {"message": "Hacker News collection complete", "discovered": len(posts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/collect/reddit")
def collect_reddit():
    try:
        posts = collect_reddit_ai_posts()
        for post in posts:
            save_community_post(post)
        return {"message": "Reddit collection complete", "discovered": len(posts)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/collect/all")
def collect_all():
    results = {}

    try:
        tools = collect_ai_tools()
        for tool in tools:
            save_ai_tool(tool)
        results["github"] = {"discovered": len(tools)}
    except Exception as e:
        results["github"] = {"error": str(e)}

    try:
        hn_posts = collect_hn_ai_posts()
        for post in hn_posts:
            save_community_post(post)
        results["hackernews"] = {"discovered": len(hn_posts)}
    except Exception as e:
        results["hackernews"] = {"error": str(e)}

    try:
        reddit_posts = collect_reddit_ai_posts()
        for post in reddit_posts:
            save_community_post(post)
        results["reddit"] = {"discovered": len(reddit_posts)}
    except Exception as e:
        results["reddit"] = {"error": str(e)}

    return {"message": "Collection complete", "results": results}


@router.get("/report")
def get_report():
    try:
        report = build_full_report()
        return {"report": report}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/stats")
def get_stats():
    with Session(engine) as session:
        tool_count = len(session.exec(select(AITool)).all())
        post_count = len(session.exec(select(CommunityPost)).all())
        news_count = len(session.exec(select(News)).all())
        return {
            "tools": tool_count,
            "posts": post_count,
            "news": news_count,
            "total": tool_count + post_count + news_count,
        }
