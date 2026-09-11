from app.services.ocr_data_parser import parse_ocr_data
from app.services.ocr_row_grouper import group_tokens_into_rows
from app.services.invoice_table_detector import detect_table_header
from app.services.invoice_table_extractor import extract_table_rows
from app.services.line_item_parser import parse_line_item
from app.utils.logger import get_logger


logger = get_logger(__name__)


def extract_line_items_from_ocr_data(ocr_data):
    """
    Extract invoice line items from positional OCR data.
    """

    # Step 1: Convert Tesseract output into structured tokens
    tokens = parse_ocr_data(ocr_data)

    if not tokens:
        return []

    # Step 2: Group tokens into visual rows
    rows = group_tokens_into_rows(tokens)

    if not rows:
        return []

    # Step 3: Find invoice table header
    header_index = detect_table_header(rows)

    if header_index is None:
        return []

    # Step 4: Extract rows belonging to the table
    table_rows = extract_table_rows(
        rows,
        header_index
    )

    if not table_rows:
        return []

    # Step 5: Parse each table row
    items = []

    for row in table_rows:

        item = parse_line_item(
            row["text"]
        )

        if item:
            items.append(item)

    logger.info(
        "Layout-aware extraction produced %d line items",
        len(items)
    )

    return items