from pathlib import Path

from automation.investigation import build_failure_context
from automation.ai_agent.error_analyzer import analyze_sql_error
from automation.ai_agent.llm_investigator import investigate_with_llm


query_file = Path(
    "automation/queries/daily_sales_test_failure.sql"
)

context = build_failure_context(
    "2018-08-29",
    query_file,
    "1054 (42S22): Unknown column 'payment_value_invalid' in 'field list'",
)

analysis = analyze_sql_error(context)

result = investigate_with_llm(
    context,
    analysis,
)

print("\nAI INVESTIGATION RESULT")
print("========================\n")
print(result)