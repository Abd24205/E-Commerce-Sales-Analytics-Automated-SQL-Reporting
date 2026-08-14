from pathlib import Path

from automation.schema_inspector import get_table_columns

BASE_DIR = Path(__file__).resolve().parent


def build_failure_context(report_date, query_file, error):
    """Build structured context for investigating a failed SQL report."""

    query = query_file.read_text(encoding="utf-8")

    columns = get_table_columns("ecommerce_dashboard")

    context = {
        "report_date": report_date,
        "query_file": query_file.name,
        "query": query,
        "error": str(error),
        "table": "ecommerce_dashboard",
        "available_columns": columns,
    }

    return context


def save_failure_context(report_date, context):
    """Save investigation context as a text file."""

    output_file = BASE_DIR / "logs" / f"{report_date}_investigation.txt"

    lines = [
        "SQL FAILURE INVESTIGATION",
        "==========================",
        f"Report Date: {context['report_date']}",
        f"Query File: {context['query_file']}",
        "",
        "ERROR:",
        context["error"],
        "",
        "TABLE:",
        context["table"],
        "",
        "QUERY:",
        context["query"],
        "",
        "AVAILABLE COLUMNS:",
    ]

    lines.extend(
        f"- {column}"
        for column in context["available_columns"]
    )

    output_file.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return output_file