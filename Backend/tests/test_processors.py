from unittest.mock import patch

import numpy as np

from app.processors.image_processor import process_image

import pytest
from app.processors.image_processor import process_image
from app.processors.pdf_processor import process_pdf

from app.processors.image_processor import process_image


def test_process_image_file_not_found():

    with pytest.raises(FileNotFoundError):

        process_image(
            "does_not_exist.jpg"
        )
from unittest.mock import patch

import numpy as np

from app.processors.image_processor import process_image


def test_process_image(tmp_path):

    # Create a temporary fake image file
    image_path = tmp_path / "fake.jpg"
    image_path.write_bytes(b"fake image content")

    fake_image = np.zeros(
        (100, 100, 3),
        dtype=np.uint8
    )

    with patch(
        "app.processors.image_processor.cv2.imread",
        return_value=fake_image
    ):

        with patch(
            "app.processors.image_processor.extract_text_from_image",
            return_value="Invoice No: INV-1001\nTotal: 5000"
        ):

            result = process_image(
                str(image_path)
            )

    assert len(result) == 1

    assert result[0]["invoice_number"] == "INV-1001"

    assert "total" in result[0]
from unittest.mock import patch
@patch(
    "app.processors.image_processor.cv2.imread"
)
@patch(
    "app.processors.image_processor.extract_ocr_data_from_image"
)
@patch(
    "app.processors.image_processor.extract_text_from_image"
)
def test_process_image_with_layout_items(
    mock_extract_text,
    mock_extract_ocr_data,
    mock_imread,
    tmp_path
):
    image_path = tmp_path / "invoice.jpg"
    image_path.write_bytes(b"fake image")

    mock_imread.return_value = object()

    mock_extract_text.return_value = """
    Invoice No: INV-1001
    Date: 10/09/2026
    """

    mock_extract_ocr_data.return_value = {
        "text": [
            "Description",
            "HSN",
            "Qty",
            "Rate",
            "Amount",
            "Laptop",
            "8471",
            "2",
            "45000",
            "90000"
        ],
        "left": [
            100, 250, 350, 450, 550,
            100, 250, 350, 450, 550
        ],
        "top": [
            100, 100, 100, 100, 100,
            200, 200, 200, 200, 200
        ],
        "width": [50] * 10,
        "height": [20] * 10,
        "conf": ["95"] * 10
    }

    result = process_image(
        str(image_path)
    )

    assert len(result) == 1

    assert result[0]["invoice_number"] == "INV-1001"

    assert len(result[0]["line_items"]) == 1

    assert (
        result[0]["line_items"][0]["description"]
        == "Laptop"
    )

    assert (
        result[0]["line_items"][0]["amount"]
        == 90000.0
    )

@patch(
    "app.processors.pdf_processor.extract_ocr_data_from_image"
)
@patch(
    "app.processors.pdf_processor.extract_text_from_image"
)
@patch(
    "app.processors.pdf_processor.convert_from_path"
)
def test_process_pdf_with_layout_items(
    mock_convert,
    mock_extract_text,
    mock_extract_ocr_data,
    tmp_path
):
    pdf_path = tmp_path / "invoice.pdf"
    pdf_path.write_bytes(b"fake pdf")

    mock_convert.return_value = [
        "fake_page"
    ]

    mock_extract_text.return_value = """
    Invoice No: INV-1001
    Date: 10/09/2026
    """

    mock_extract_ocr_data.return_value = {
        "text": [
            "Description",
            "HSN",
            "Qty",
            "Rate",
            "Amount",
            "Laptop",
            "8471",
            "2",
            "45000",
            "90000"
        ],
        "left": [
            100, 250, 350, 450, 550,
            100, 250, 350, 450, 550
        ],
        "top": [
            100, 100, 100, 100, 100,
            200, 200, 200, 200, 200
        ],
        "width": [50] * 10,
        "height": [20] * 10,
        "conf": ["95"] * 10
    }

    result = process_pdf(
        str(pdf_path)
    )

    assert len(result) == 1

    assert (
        result[0]["invoice_number"]
        == "INV-1001"
    )

    assert len(result[0]["line_items"]) == 1

    assert (
        result[0]["line_items"][0]["description"]
        == "Laptop"
    )

    assert (
        result[0]["line_items"][0]["amount"]
        == 90000.0
    )