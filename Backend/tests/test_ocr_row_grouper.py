from app.services.ocr_row_grouper import (
    group_tokens_into_rows
)


def test_group_tokens_into_rows():

    tokens = [
        {
            "text": "Laptop",
            "x": 100,
            "y": 450,
            "width": 50,
            "height": 20,
            "confidence": 95
        },
        {
            "text": "8471",
            "x": 300,
            "y": 452,
            "width": 40,
            "height": 20,
            "confidence": 96
        },
        {
            "text": "2",
            "x": 400,
            "y": 449,
            "width": 20,
            "height": 20,
            "confidence": 97
        },
        {
            "text": "90000",
            "x": 600,
            "y": 700,
            "width": 60,
            "height": 20,
            "confidence": 98
        }
    ]

    result = group_tokens_into_rows(tokens)

    assert len(result) == 2

    assert result[0]["text"] == "Laptop 8471 2"
    assert result[1]["text"] == "90000"


def test_tokens_are_sorted_left_to_right():

    tokens = [
        {
            "text": "90000",
            "x": 600,
            "y": 450,
            "width": 60,
            "height": 20,
            "confidence": 98
        },
        {
            "text": "Laptop",
            "x": 100,
            "y": 450,
            "width": 50,
            "height": 20,
            "confidence": 95
        }
    ]

    result = group_tokens_into_rows(tokens)

    assert result[0]["text"] == "Laptop 90000"


def test_empty_tokens():

    result = group_tokens_into_rows([])

    assert result == []