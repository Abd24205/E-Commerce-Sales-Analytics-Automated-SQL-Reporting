import re


def analyze_sql_error(context):
    """Determine factual information about a SQL failure."""

    error = context["error"]
    columns = context["available_columns"]

    result = {
        "error_type": "UNKNOWN",
        "invalid_column": None,
        "column_exists": None,
        "root_cause": "Unable to determine root cause.",
        "severity": "HIGH",
    }

    match = re.search(
        r"unknown column ['`]?([^'` ]+)['`]?",
        error,
        re.IGNORECASE,
    )

    if match:
        invalid_column = match.group(1)

        result["error_type"] = "UNKNOWN_COLUMN"
        result["invalid_column"] = invalid_column
        result["column_exists"] = invalid_column in columns

        if not result["column_exists"]:
            result["root_cause"] = (
                f"The SQL query references the column "
                f"'{invalid_column}', but that column does not "
                f"exist in the 'ecommerce_dashboard' table."
            )

    return result