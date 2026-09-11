import cv2

from app.services.ocr_service import (
    extract_text_from_image,
    extract_ocr_data_from_image
)

from app.services.invoice_parser import parse_invoice_text

from app.services.layout_invoice_parser import (
    extract_line_items_from_ocr_data
)

from app.utils.logger import get_logger
from app.utils.validators import validate_image_file


logger = get_logger(__name__)


def process_image(file_path):
    """
    Process an invoice image.
    """

    logger.info(
        "Processing image: %s",
        file_path
    )

    # Validate file
    validate_image_file(file_path)

    # Read image
    image = cv2.imread(file_path)

    if image is None:

        logger.error(
            "OpenCV could not read image: %s",
            file_path
        )

        raise ValueError(
            f"Unable to read image: {file_path}"
        )

    try:

        # Extract normal OCR text
        text = extract_text_from_image(
            image,
            augment=True
        )

        # Extract structured invoice fields
        data = parse_invoice_text(
            text
        )

        # Extract positional OCR information
        ocr_data = extract_ocr_data_from_image(
            image
        )

        # Extract line items using layout information
        data["line_items"] = (
            extract_line_items_from_ocr_data(
                ocr_data
            )
        )

        logger.info(
            "Image processing completed successfully"
        )

        return [data]

    except Exception:

        logger.exception(
            "Image processing failed: %s",
            file_path
        )

        raise