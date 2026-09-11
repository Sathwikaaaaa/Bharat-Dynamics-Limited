from app.utils.logger import get_logger

logger = get_logger(__name__)


TABLE_HEADER_KEYWORDS = {
    "description",
    "qty",
    "quantity",
    "rate",
    "amount",
    "hsn",
    "hsn code",
}


def normalize_text(text):
    return " ".join(text.lower().split())


def detect_table_header(rows):
    """
    Find the row that most likely represents
    the invoice line-item table header.
    """

    for index, row in enumerate(rows):

        text = normalize_text(row["text"])

        matched_keywords = 0

        for keyword in TABLE_HEADER_KEYWORDS:
            if keyword in text:
                matched_keywords += 1

        # Require at least 3 table-related keywords.
        if matched_keywords >= 3:

            logger.info(
                "Invoice table header detected at row %d: %s",
                index,
                row["text"]
            )

            return index

    logger.info("Invoice table header not detected")

    return None