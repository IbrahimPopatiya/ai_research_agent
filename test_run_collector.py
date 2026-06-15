from database.db import create_db_and_tables
from collectors.github_collector import collect_and_store_ai_tools

# create tables first
create_db_and_tables()

# run collector
collect_and_store_ai_tools()