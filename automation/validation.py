def validate_daily_sales(result):
    """Validate the daily sales report result."""

    errors = []

    if not result:
        errors.append("No report data was returned.")

        return errors

    if result.get("total_sales") is None:
        errors.append("Total sales is NULL.")

    if result.get("total_orders") is None:
        errors.append("Total orders is NULL.")

    elif result["total_orders"] <= 0:
        errors.append("Total orders must be greater than zero.")

    if result.get("average_order_value") is None:
        errors.append("Average order value is NULL.")

    elif result["average_order_value"] < 0:
        errors.append("Average order value cannot be negative.")

    return errors