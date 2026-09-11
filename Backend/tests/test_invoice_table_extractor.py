from app.services.invoice_table_extractor import (
    extract_table_rows
)


def test_extract_table_rows():

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
        },
        {
            "y": 300,
            "text": "Mouse 8471 3 500 1500",
            "tokens": []
        },
        {
            "y": 400,
            "text": "Subtotal 91500",
            "tokens": []
        },
        {
            "y": 450,
            "text": "GST 16470",
            "tokens": []
        }
    ]

    result = extract_table_rows(rows, 1)

    assert len(result) == 2

    assert result[0]["text"] == (
        "Laptop 8471 2 45000 90000"
    )

    assert result[1]["text"] == (
        "Mouse 8471 3 500 1500"
    )


def test_stop_at_total():

    rows = [
        {
            "y": 100,
            "text": "Description HSN Qty Rate Amount",
            "tokens": []
        },
        {
            "y": 200,
            "text": "Laptop 8471 1 50000 50000",
            "tokens": []
        },
        {
            "y": 300,
            "text": "Grand Total 50000",
            "tokens": []
        },
        {
            "y": 350,
            "text": "Another row",
            "tokens": []
        }
    ]

    result = extract_table_rows(rows, 0)

    assert len(result) == 1
    assert result[0]["text"] == (
        "Laptop 8471 1 50000 50000"
    )


def test_no_header():

    rows = [
        {
            "y": 100,
            "text": "Laptop 8471 1 50000 50000",
            "tokens": []
        }
    ]

    result = extract_table_rows(rows, None)

    assert result == []