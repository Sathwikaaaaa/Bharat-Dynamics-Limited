from unittest.mock import patch

import numpy as np

from app.services.ocr_service import extract_ocr_data_from_image


@patch("app.services.ocr_service.pytesseract.image_to_data")
@patch("app.services.ocr_service.preprocess_image")
def test_extract_ocr_data_from_image(
    mock_preprocess,
    mock_image_to_data
):
    mock_preprocess.return_value = np.zeros(
        (100, 100),
        dtype=np.uint8
    )

    mock_image_to_data.return_value = {
        "text": ["Invoice", "INV-1001"],
        "left": [10, 100],
        "top": [20, 20],
        "width": [50, 80],
        "height": [20, 20],
        "conf": ["95", "98"]
    }

    image = np.zeros(
        (100, 100, 3),
        dtype=np.uint8
    )

    result = extract_ocr_data_from_image(image)

    assert "text" in result
    assert "left" in result
    assert "top" in result

    assert result["text"][0] == "Invoice"
    assert result["text"][1] == "INV-1001"