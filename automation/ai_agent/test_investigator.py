from pathlib import Path

from automation.investigation import build_failure_context
from automation.ai_agent.investigator import investigate_failure


query_file = Path(
    "automation/queries/daily_sales_test_failure.sql"
)

context = build_failure_context(
    "2018-08-29",
    query_file,
    "1054 (42S22): Unknown column 'payment_value_invalid' in 'field list'",
)

diagnosis = investigate_failure(context)

print("\nAI INVESTIGATION RESULT")
print("========================")

print(f"\nRoot Cause:\n{diagnosis['root_cause']}")

print("\nEvidence:")
for evidence in diagnosis["evidence"]:
    print(f"- {evidence}")

print(f"\nSuggested Fix:\n{diagnosis['suggested_fix']}")

print(f"\nSeverity:\n{diagnosis['severity']}")