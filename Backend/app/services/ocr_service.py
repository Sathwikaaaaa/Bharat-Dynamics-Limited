import pytesseract

from app.services.preprocessing import preprocess_image
from app.utils.config import TESSERACT_CMD
from app.utils.logger import get_logger


logger = get_logger(__name__)


pytesseract.pytesseract.tesseract_cmd = TESSERACT_CMD


def extract_text_from_image(image, augment=False):
    """
    Extract text from an image using Tesseract OCR.
    """

    logger.info("Starting OCR extraction")

    try:
        preprocessed = preprocess_image(
            image,
            augment=augment
        )

        text = pytesseract.image_to_string(
            preprocessed
        )

        logger.info(
            "OCR extraction completed successfully"
        )

        return text

    except Exception:
        logger.exception(
            "OCR extraction failed"
        )

        raise

def extract_ocr_data_from_image(image):
    logger.info("Starting positional OCR extraction")

    processed_image = preprocess_image(image)

    try:
        ocr_data = pytesseract.image_to_data(
            processed_image,
            output_type=pytesseract.Output.DICT
        )

        logger.info("Positional OCR extraction completed")

        return ocr_data

    except Exception:
        logger.exception("Positional OCR extraction failed")
        raise