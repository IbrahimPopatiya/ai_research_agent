from database.db import create_db_and_tables
from analysis.research_analyzer import run_analysis

create_db_and_tables()

report = run_analysis()
print("\n===== AI RESEARCH REPORT =====\n")

print(report)