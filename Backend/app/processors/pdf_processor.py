import cv2
import numpy as np

from pdf2image import convert_from_path

from app.services.ocr_service import (
    extract_text_from_image,
    extract_ocr_data_from_image
)

from app.services.invoice_parser import parse_invoice_text

from app.services.layout_invoice_parser import (
    extract_line_items_from_ocr_data
)

from app.utils.validators import validate_pdf_file
from app.utils.logger import get_logger


logger = get_logger(__name__)


def process_pdf(file_path):
    """
    Process a PDF invoice.

    Flow:
        PDF
        ↓
        PDF pages → PIL images
        ↓
        PIL → OpenCV images
        ↓
        OCR text + positional OCR data
        ↓
        Header extraction + layout-aware line-item extraction
        ↓
        Invoice data
    """

    validate_pdf_file(file_path)

    logger.info(
        "Starting PDF processing: %s",
        file_path
    )

    try:

        pages = convert_from_path(file_path)

        results = []

        for page_number, page in enumerate(
            pages,
            start=1
        ):

            logger.info(
                "Processing PDF page %d",
                page_number
            )

            # -------------------------------------------------
            # Convert PIL Image → NumPy/OpenCV image
            # -------------------------------------------------

            page_array = np.array(page)

            page_image = cv2.cvtColor(
                page_array,
                cv2.COLOR_RGB2BGR
            )

            # -------------------------------------------------
            # 1. Extract normal OCR text
            # -------------------------------------------------

            ocr_text = extract_text_from_image(
                page_image
            )

            # -------------------------------------------------
            # 2. Extract structured invoice/header fields
            # -------------------------------------------------

            invoice_data = parse_invoice_text(
                ocr_text
            )

            # -------------------------------------------------
            # 3. Extract positional OCR data
            # -------------------------------------------------

            ocr_data = extract_ocr_data_from_image(
                page_image
            )

            # -------------------------------------------------
            # 4. Extract line items using layout information
            # -------------------------------------------------

            invoice_data["line_items"] = (
                extract_line_items_from_ocr_data(
                    ocr_data
                )
            )

            results.append(
                invoice_data
            )

            logger.info(
                "PDF page %d processed successfully",
                page_number
            )

        logger.info(
            "PDF processing completed: %s",
            file_path
        )

        return results

    except Exception:

        logger.exception(
            "PDF processing failed: %s",
            file_path
        )

        raise