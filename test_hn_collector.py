from database.db import create_db_and_tables
from collectors.hackernews_collector import collect_hn_ai_posts
from database.crud import save_community_post

create_db_and_tables()

posts = collect_hn_ai_posts()

for post in posts:
    save_community_post(post)