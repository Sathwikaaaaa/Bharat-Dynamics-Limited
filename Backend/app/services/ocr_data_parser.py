from app.utils.logger import get_logger

logger = get_logger(__name__)


def parse_ocr_data(ocr_data):
    """
    Convert Tesseract's dictionary output into
    a list of structured OCR tokens.
    """

    tokens = []

    texts = ocr_data.get("text", [])
    left = ocr_data.get("left", [])
    top = ocr_data.get("top", [])
    width = ocr_data.get("width", [])
    height = ocr_data.get("height", [])
    confidence = ocr_data.get("conf", [])

    for i, text in enumerate(texts):

        text = text.strip()

        if not text:
            continue

        try:
            conf = float(confidence[i])
        except (ValueError, TypeError, IndexError):
            conf = 0.0

        token = {
            "text": text,
            "x": left[i],
            "y": top[i],
            "width": width[i],
            "height": height[i],
            "confidence": conf
        }

        tokens.append(token)

    logger.info(
        "Parsed %d OCR tokens",
        len(tokens)
    )

    return tokens