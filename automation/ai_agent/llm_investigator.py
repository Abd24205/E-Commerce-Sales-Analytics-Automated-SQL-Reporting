import ollama


MODEL = "llama3.2:3b"


def investigate_with_llm(context, analysis):
    """Explain verified SQL failure facts using the local LLM."""

    prompt = f"""
You are a data engineering incident assistant.

Explain the VERIFIED findings below to a data analyst.

Do not change, contradict, or add to these facts.
Do not invent causes.
Do not suggest changes to data unless explicitly supported.
Do not claim that a SQL query needs every database column.

Use exactly these headings:

ROOT CAUSE:
EVIDENCE:
SUGGESTED FIX:
SEVERITY:

VERIFIED ERROR TYPE:
{analysis["error_type"]}

VERIFIED INVALID COLUMN:
{analysis["invalid_column"]}

DOES THE COLUMN EXIST:
{analysis["column_exists"]}

VERIFIED ROOT CAUSE:
{analysis["root_cause"]}

VERIFIED SEVERITY:
{analysis["severity"]}

SQL ERROR:
{context["error"]}

AVAILABLE COLUMNS:
{", ".join(context["available_columns"])}

The correct suggested fix should address the verified root cause.
Keep the response concise.
"""

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response["message"]["content"].strip()