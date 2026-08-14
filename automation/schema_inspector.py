from automation.database import get_connection

def get_table_columns(table_name):
    """Return column names for a MySQL table."""

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(f"DESCRIBE `{table_name}`")

        columns = [row[0] for row in cursor.fetchall()]

        return columns

    finally:
        cursor.close()
        connection.close()


if __name__ == "__main__":
    columns = get_table_columns("ecommerce_dashboard")

    print("Available columns:")
    for column in columns:
        print(f"- {column}")