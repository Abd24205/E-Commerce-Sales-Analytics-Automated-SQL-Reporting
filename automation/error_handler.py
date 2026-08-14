from datetime import datetime
from pathlib import Path


LOG_DIR = Path(__file__).resolve().parent / "logs"


def log_failure(report_date, error, query_file):
    """Save structured information about a failed report."""

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().isoformat(timespec="seconds")

    log_file = LOG_DIR / f"{report_date}_failure.log"

    content = f"""REPORT FAILURE
========================
Timestamp: {timestamp}
Report Date: {report_date}
Query: {query_file}

Error:
{error}
"""

    log_file.write_text(content, encoding="utf-8")

    return log_file