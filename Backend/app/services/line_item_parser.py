import re

from app.utils.logger import get_logger

logger = get_logger(__name__)


def extract_number(value):
    if not value:
        return None

    value = value.replace(",", "")

    match = re.search(r"-?\d+(?:\.\d+)?", value)

    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None


def parse_line_item(line):
    """
    Parse a single OCR line representing an invoice item.

    Expected general structure:

    Description HSN Qty Rate Amount
    """

    line = line.strip()

    if not line:
        return None

    # Look for numeric values at the end of the line.
    numbers = re.findall(
        r"-?\d+(?:,\d{3})*(?:\.\d+)?",
        line
    )

    if len(numbers) < 3:
        return None

    try:
        amount = float(numbers[-1].replace(",", ""))
        unit_price = float(numbers[-2].replace(",", ""))
        quantity = float(numbers[-3].replace(",", ""))
    except ValueError:
        return None

    description_part = line[:line.rfind(numbers[-3])].strip()

    if not description_part:
        return None

    hsn_code = None

    hsn_match = re.search(
        r"\b\d{4,8}\b",
        description_part
    )

    if hsn_match:
        hsn_code = hsn_match.group()
        description = (
            description_part[:hsn_match.start()]
            + description_part[hsn_match.end():]
        ).strip()
    else:
        description = description_part

    item = {
        "description": description,
        "hsn_code": hsn_code,
        "quantity": quantity,
        "unit_price": unit_price,
        "amount": amount
    }

    logger.info("Line item extracted: %s", item)

    return item