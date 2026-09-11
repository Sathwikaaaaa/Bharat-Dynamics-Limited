from app.utils.logger import get_logger

logger = get_logger(__name__)


STOP_KEYWORDS = {
    "subtotal",
    "sub total",
    "taxable value",
    "cgst",
    "sgst",
    "igst",
    "grand total",
    "total amount",
    "amount in words",
    "authorised signature",
    "authorized signature",
}


def extract_table_rows(rows, header_index):
    """
    Extract rows appearing after the detected table header.

    Extraction stops when an invoice total/tax section begins.
    """

    if header_index is None:
        return []

    table_rows = []

    for row in rows[header_index + 1:]:

        text = row["text"].strip()

        if not text:
            continue

        lower_text = text.lower()

        if any(
            keyword in lower_text
            for keyword in STOP_KEYWORDS
        ):
            break

        table_rows.append(row)

    logger.info(
        "Extracted %d invoice table rows",
        len(table_rows)
    )

    return table_rows