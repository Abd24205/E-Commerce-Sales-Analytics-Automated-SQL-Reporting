import json
import sys
from datetime import date
from pathlib import Path

from automation.database import get_connection
from automation.validation import validate_daily_sales
from automation.error_handler import log_failure

from automation.investigation import build_failure_context
from automation.ai_agent.error_analyzer import analyze_sql_error
from automation.ai_agent.llm_investigator import investigate_with_llm


BASE_DIR = Path(__file__).resolve().parent
QUERY_FILE = BASE_DIR / "queries" / "daily_sales.sql"
REPORT_DIR = BASE_DIR / "reports"
AI_REPORT_DIR = BASE_DIR / "logs"


def load_query():
    """Load the SQL query from the query file."""
    return QUERY_FILE.read_text(encoding="utf-8")


def run_daily_sales(report_date, query_file=QUERY_FILE):
    """Run a sales query for the supplied date."""

    query = query_file.read_text(encoding="utf-8")
    connection = get_connection()

    try:
        cursor = connection.cursor(dictionary=True)

        cursor.execute(query, (report_date,))
        result = cursor.fetchone()

        return result

    finally:
        cursor.close()
        connection.close()


def save_report(report_date, result):
    """Save the report result as JSON."""

    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = REPORT_DIR / f"{report_date}_daily_sales.json"

    report = {
        "report_date": str(report_date),
        "report_type": "daily_sales",
        "status": "success",
        "metrics": result,
    }

    output_file.write_text(
        json.dumps(report, indent=4, default=str),
        encoding="utf-8",
    )

    return output_file


def save_ai_investigation(report_date, analysis, ai_result):
    """Save the AI investigation report."""

    AI_REPORT_DIR.mkdir(parents=True, exist_ok=True)

    output_file = (
        AI_REPORT_DIR
        / f"{report_date}_ai_investigation.txt"
    )

    content = [
        "AI SQL FAILURE INVESTIGATION",
        "============================",
        f"Report Date: {report_date}",
        "",
        "DETERMINISTIC ANALYSIS",
        "-----------------------",
        f"Error Type: {analysis['error_type']}",
        f"Invalid Column: {analysis['invalid_column']}",
        f"Column Exists: {analysis['column_exists']}",
        f"Root Cause: {analysis['root_cause']}",
        f"Severity: {analysis['severity']}",
        "",
        "LLM INVESTIGATION",
        "-----------------",
        ai_result,
        "",
    ]

    output_file.write_text(
        "\n".join(content),
        encoding="utf-8",
    )

    return output_file


def main():
    if len(sys.argv) not in (2, 3):
        print("Usage: python automation/runner.py YYYY-MM-DD")
        sys.exit(1)

    report_date = sys.argv[1]

    try:
        date.fromisoformat(report_date)
    except ValueError:
        print("Invalid date. Use YYYY-MM-DD.")
        sys.exit(1)

    print(f"Running Daily Sales Report for {report_date}...")

    query_file = QUERY_FILE

    if len(sys.argv) == 3 and sys.argv[2] == "--test-failure":
        query_file = (
            BASE_DIR
            / "queries"
            / "daily_sales_test_failure.sql"
        )

        print("Running controlled failure test...")

    try:
        result = run_daily_sales(
            report_date,
            query_file,
        )

    except Exception as error:
        print("\nREPORT FAILED")
        print(f"Error: {error}")

        # Existing failure logging.
        log_file = log_failure(
            report_date,
            error,
            query_file.name,
        )

        print(f"Failure logged to: {log_file}")

        # Build investigation context.
        print("\nBuilding failure investigation...")

        try:
            context = build_failure_context(
                report_date,
                query_file,
                error,
            )

            # Deterministic analysis.
            analysis = analyze_sql_error(context)

            print("\nDeterministic analysis complete.")
            print(f"Root Cause: {analysis['root_cause']}")
            print(f"Severity: {analysis['severity']}")

            # Local LLM investigation.
            print("\nRunning AI investigation...")

            ai_result = investigate_with_llm(
                context,
                analysis,
            )

            # Save final AI investigation.
            ai_report = save_ai_investigation(
                report_date,
                analysis,
                ai_result,
            )

            print("\nAI investigation completed.")
            print(f"AI Report: {ai_report}")

        except Exception as investigation_error:
            print(
                "\nWARNING: AI investigation failed."
            )
            print(f"Investigation error: {investigation_error}")

        sys.exit(1)

    if not result:
        print(f"No sales data found for {report_date}.")
        sys.exit(1)

    validation_errors = validate_daily_sales(result)

    if validation_errors:
        print("\nReport validation FAILED:")

        for error in validation_errors:
            print(f"- {error}")

        sys.exit(1)

    report_file = save_report(
        report_date,
        result,
    )

    print("\nReport generated successfully.")
    print(f"Total Sales: {result['total_sales']}")
    print(f"Total Orders: {result['total_orders']}")
    print(
        f"Average Order Value: "
        f"{result['average_order_value']}"
    )
    print(f"\nSaved to: {report_file}")


if __name__ == "__main__":
    main()