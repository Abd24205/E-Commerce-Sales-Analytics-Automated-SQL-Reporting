import re


def investigate_failure(context):
    """
    Analyze a SQL failure context and return a structured diagnosis.
    """

    error = context["error"]
    query = context["query"]
    available_columns = context["available_columns"]

    diagnosis = {
        "status": "investigation_complete",
        "root_cause": "Unknown",
        "evidence": [],
        "suggested_fix": "Review the failed SQL query.",
        "severity": "MEDIUM",
    }

    # Detect unknown-column errors.
    match = re.search(
        r"unknown column ['`]?([^'` ]+)['`]?",
        error,
        re.IGNORECASE,
    )

    if match:
        invalid_column = match.group(1)

        diagnosis["root_cause"] = (
            f"The SQL query references a column that does not exist: "
            f"{invalid_column}"
        )

        diagnosis["evidence"].append(
            f"Invalid column referenced: {invalid_column}"
        )

        if invalid_column not in available_columns:
            diagnosis["evidence"].append(
                f"{invalid_column} is not present in the "
                f"ecommerce_dashboard schema."
            )

        # Look for likely column matches.
        if "payment_value" in available_columns:
            if "payment_value" in query:
                diagnosis["suggested_fix"] = (
                    f"Replace {invalid_column} with payment_value "
                    "if the intended metric is payment value."
                )

        diagnosis["severity"] = "HIGH"

    return diagnosis