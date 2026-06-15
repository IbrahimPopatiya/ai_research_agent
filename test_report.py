from database.db import create_db_and_tables
from reports.report_builder import build_full_report

create_db_and_tables()

report = build_full_report()

print(report)