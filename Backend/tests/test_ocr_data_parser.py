from app.services.ocr_data_parser import parse_ocr_data


def test_parse_ocr_data():
    ocr_data = {
        "text": [
            "",
            "Invoice",
            "INV-1001"
        ],
        "left": [
            0,
            10,
            100
        ],
        "top": [
            0,
            20,
            20
        ],
        "width": [
            0,
            50,
            80
        ],
        "height": [
            0,
            20,
            20
        ],
        "conf": [
            "-1",
            "95.5",
            "98.0"
        ]
    }

    result = parse_ocr_data(ocr_data)

    assert len(result) == 2

    assert result[0]["text"] == "Invoice"
    assert result[0]["x"] == 10
    assert result[0]["y"] == 20
    assert result[0]["confidence"] == 95.5

    assert result[1]["text"] == "INV-1001"
    assert result[1]["x"] == 100
    assert result[1]["y"] == 20
    assert result[1]["confidence"] == 98.0


def test_empty_ocr_data():
    ocr_data = {
        "text": [],
        "left": [],
        "top": [],
        "width": [],
        "height": [],
        "conf": []
    }

    result = parse_ocr_data(ocr_data)

    assert result == []


def test_low_confidence_token_is_preserved():
    ocr_data = {
        "text": ["Invoice"],
        "left": [10],
        "top": [20],
        "width": [50],
        "height": [20],
        "conf": ["30"]
    }

    result = parse_ocr_data(ocr_data)

    assert len(result) == 1
    assert result[0]["confidence"] == 30.0