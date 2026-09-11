from app.services.layout_invoice_parser import (
    extract_line_items_from_ocr_data
)


def test_layout_invoice_parser():

    ocr_data = {
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
            "90000",
            "Mouse",
            "8471",
            "3",
            "500",
            "1500",
            "Subtotal",
            "91500"
        ],

        "left": [
            100,
            250,
            350,
            450,
            550,
            100,
            250,
            350,
            450,
            550,
            100,
            250,
            350,
            450,
            550,
            100,
            100
        ],

        "top": [
            100,
            100,
            100,
            100,
            100,
            200,
            200,
            200,
            200,
            200,
            300,
            300,
            300,
            300,
            300,
            400,
            400
        ],

        "width": [50] * 17,

        "height": [20] * 17,

        "conf": ["95"] * 17
    }

    result = extract_line_items_from_ocr_data(
        ocr_data
    )

    assert len(result) == 2

    assert result[0]["description"] == "Laptop"
    assert result[0]["hsn_code"] == "8471"
    assert result[0]["quantity"] == 2.0
    assert result[0]["unit_price"] == 45000.0
    assert result[0]["amount"] == 90000.0

    assert result[1]["description"] == "Mouse"
    assert result[1]["hsn_code"] == "8471"
    assert result[1]["quantity"] == 3.0
    assert result[1]["amount"] == 1500.0


def test_layout_parser_with_empty_ocr():

    ocr_data = {
        "text": [],
        "left": [],
        "top": [],
        "width": [],
        "height": [],
        "conf": []
    }

    result = extract_line_items_from_ocr_data(
        ocr_data
    )

    assert result == []