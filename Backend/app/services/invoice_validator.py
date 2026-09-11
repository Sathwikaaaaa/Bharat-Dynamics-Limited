import re

from app.utils.logger import get_logger

logger = get_logger(__name__)


GSTIN_PATTERN = re.compile(
    r"^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$"
)

def validate_line_items(line_items):
    errors = []

    for index, item in enumerate(line_items):
        quantity = item.get("quantity")
        unit_price = item.get("unit_price")
        amount = item.get("amount")

        if (
            quantity is None
            or unit_price is None
            or amount is None
        ):
            continue

        expected_amount = quantity * unit_price

        if abs(expected_amount - amount) > 0.01:
            errors.append(
                f"Line item {index + 1}: "
                "quantity × unit price does not match amount."
            )

    return errors
def validate_invoice(data):
    errors = []
    line_items = data.get("line_items", [])

    errors.extend(
        validate_line_items(line_items)
    )

    if not data.get("invoice_number"):
        errors.append("Invoice number is missing.")

    if not data.get("invoice_date"):
        errors.append("Invoice date is missing.")

    gstin = data.get("gstin")

    if gstin and not GSTIN_PATTERN.match(gstin):
        errors.append("Invalid GSTIN format.")

    for field in ["subtotal", "tax", "total"]:
        value = data.get(field)

        if value is not None and value < 0:
            errors.append(
                f"{field} cannot be negative."
            )

    subtotal = data.get("subtotal")
    tax = data.get("tax")
    total = data.get("total")

    if (
        subtotal is not None
        and tax is not None
        and total is not None
    ):
        calculated_total = subtotal + tax

        if abs(calculated_total - total) > 0.01:
            errors.append(
                "Subtotal + tax does not match total."
            )

    result = {
        "is_valid": len(errors) == 0,
        "errors": errors
    }

    logger.info(
        "Invoice validation completed. Valid=%s",
        result["is_valid"]
    )

    return result