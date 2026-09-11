import re

from app.utils.logger import get_logger
from app.services.line_item_parser import parse_line_item

logger = get_logger(__name__)


def clean_text(value):
    """
    Clean extracted OCR text.
    """

    if not value:
        return None

    value = value.strip()

    value = re.sub(
        r"\s+",
        " ",
        value
    )

    return value


def extract_value(
    lines,
    patterns
):
    """
    Search invoice lines using a list of regex patterns.
    """

    for line in lines:

        for pattern in patterns:

            match = re.search(
                pattern,
                line,
                re.IGNORECASE
            )

            if match:
                return clean_text(
                    match.group(1)
                )

    return None


def extract_number(value):
    """
    Extract a numeric value from OCR text.
    """

    if not value:
        return None

    value = value.replace(",", "")

    match = re.search(
        r"-?\d+(?:\.\d+)?",
        value
    )

    if not match:
        return None

    try:
        return float(match.group())
    except ValueError:
        return None


def parse_invoice_text(text):
    """
    Parse OCR text and extract structured invoice information.
    """

    logger.info(
        "Starting structured invoice parsing"
    )

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    data = {}

    # --------------------------------------------------
    # Invoice number
    # --------------------------------------------------

    data["invoice_number"] = extract_value(
        lines,
        [
            r"invoice\s*(?:#|no\.?|number)?\s*[:#-]?\s*(\S+)"
        ]
    )

    # --------------------------------------------------
    # Order number
    # --------------------------------------------------

    data["order_number"] = extract_value(
        lines,
        [
            r"order\s*(?:#|no\.?|number)?\s*[:#-]?\s*(\S+)"
        ]
    )

    # --------------------------------------------------
    # Invoice date
    # --------------------------------------------------

    data["invoice_date"] = extract_value(
        lines,
        [
            r"date\s*[:#-]?\s*(.+)",
            r"invoice\s*date\s*[:#-]?\s*(.+)"
        ]
    )

    # --------------------------------------------------
    # PO number
    # --------------------------------------------------

    data["po_number"] = extract_value(
        lines,
        [
            r"(?:po|p\.o\.|purchase\s*order)"
            r"\s*(?:#|no\.?|number)?"
            r"\s*[:#-]?\s*(\S+)"
        ]
    )

    # --------------------------------------------------
    # GSTIN
    # --------------------------------------------------

    gstin = extract_value(
        lines,
        [
            r"\b([0-9]{2}[A-Z]{5}[0-9]{4}"
            r"[A-Z][1-9A-Z]Z[0-9A-Z])\b"
        ]
    )

    data["gstin"] = gstin

    # --------------------------------------------------
    # Vendor
    # --------------------------------------------------

    data["vendor"] = extract_value(
        lines,
        [
            r"(?:vendor|seller|supplier)"
            r"\s*[:#-]?\s*(.+)"
        ]
    )

    # --------------------------------------------------
    # Customer
    # --------------------------------------------------

    data["customer"] = extract_value(
        lines,
        [
            r"(?:customer|buyer|bill\s*to)"
            r"\s*[:#-]?\s*(.+)"
        ]
    )

    # --------------------------------------------------
    # Currency
    # --------------------------------------------------

    currency = None

    for line in lines:

        if "₹" in line or "rs" in line.lower():
            currency = "INR"
            break

        if "$" in line:
            currency = "USD"
            break

        if "€" in line:
            currency = "EUR"
            break

        if "£" in line:
            currency = "GBP"
            break

    data["currency"] = currency

    # --------------------------------------------------
    # Subtotal
    # --------------------------------------------------

    subtotal_text = extract_value(
        lines,
        [
            r"subtotal\s*[:#-]?\s*(.+)",
            r"sub\s*total\s*[:#-]?\s*(.+)"
        ]
    )

    data["subtotal"] = extract_number(
        subtotal_text
    )

    # --------------------------------------------------
    # Tax
    # --------------------------------------------------

    tax_text = extract_value(
        lines,
        [
            r"(?:tax|gst|cgst|sgst|igst)"
            r"\s*[:#-]?\s*(.+)"
        ]
    )

    data["tax"] = extract_number(
        tax_text
    )

    # --------------------------------------------------
    # Total
    # --------------------------------------------------

    total_text = extract_value(
        lines,
        [
            r"(?:grand\s*)?total"
            r"\s*[:#-]?\s*(.+)"
        ]
    )

    data["total"] = extract_number(
        total_text
    )

    # --------------------------------------------------
    # Line items
    # --------------------------------------------------

    data["line_items"] = extract_line_items(lines)

    data["raw_text"] = text

    logger.info(
        "Structured invoice parsing completed"
    )

    return data

def extract_line_items(lines):
    items = []

    table_started = False

    for line in lines:

        lower_line = line.lower()

        # Detect the beginning of the invoice table
        if (
            "description" in lower_line
            and (
                "qty" in lower_line
                or "quantity" in lower_line
            )
        ):
            table_started = True
            continue

        if not table_started:
            continue

        # Stop when we reach invoice totals
        if any(
            keyword in lower_line
            for keyword in [
                "subtotal",
                "sub total",
                "taxable value",
                "grand total",
                "total amount",
                "amount in words",
                "authorised signature"
            ]
        ):
            break

        item = parse_line_item(line)

        if item:
            items.append(item)

    return items