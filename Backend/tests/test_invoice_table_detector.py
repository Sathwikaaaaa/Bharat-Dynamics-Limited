from app.services.invoice_table_detector import (
    detect_table_header
)


def test_detect_table_header():

    rows = [
        {
            "y": 100,
            "text": "Tax Invoice",
            "tokens": []
        },
        {
            "y": 200,
            "text": "Description HSN Qty Rate Amount",
            "tokens": []
        },
        {
            "y": 250,
            "text": "Laptop 8471 2 45000 90000",
            "tokens": []
        }
    ]

    result = detect_table_header(rows)

    assert result == 1


def test_detect_table_header_with_quantity():

    rows = [
        {
            "y": 100,
            "text": "BLUE SKY INDIA LIMITED",
            "tokens": []
        },
        {
            "y": 300,
            "text": "Description HSN Code Quantity Rate Amount",
            "tokens": []
        }
    ]

    result = detect_table_header(rows)

    assert result == 1


def test_no_table_header():

    rows = [
        {
            "y": 100,
            "text": "Tax Invoice",
            "tokens": []
        },
        {
            "y": 200,
            "text": "Client Name TECHGURUPLUS",
            "tokens": []
        }
    ]

    result = detect_table_header(rows)

    assert result is None