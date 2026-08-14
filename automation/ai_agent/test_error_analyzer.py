from pathlib import Path

from automation.investigation import build_failure_context
from automation.ai_agent.error_analyzer import analyze_sql_error


query_file = Path(
    "automation/queries/daily_sales_test_failure.sql"
)

context = build_failure_context(
    "2018-08-29",
    query_file,
    "1054 (42S22): Unknown column 'payment_value_invalid' in 'field list'",
)

result = analyze_sql_error(context)

print("\nDETERMINISTIC ERROR ANALYSIS")
print("============================")

for key, value in result.items():
    print(f"{key}: {value}")