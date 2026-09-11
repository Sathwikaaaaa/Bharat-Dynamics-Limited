from app.services.invoice_validator import validate_invoice

from app.services.invoice_validator import (
    validate_invoice,
    validate_line_items
)
def test_valid_invoice():
    data = {
        "invoice_number": "INV-1001",
        "invoice_date": "10/09/2026",
        "gstin": "07PDUJS4678K1Z4",
        "subtotal": 4500.0,
        "tax": 500.0,
        "total": 5000.0
    }

    result = validate_invoice(data)

    assert result["is_valid"] is True
    assert result["errors"] == []


def test_missing_invoice_number():
    data = {
        "invoice_date": "10/09/2026"
    }

    result = validate_invoice(data)

    assert result["is_valid"] is False
    assert "Invoice number is missing." in result["errors"]


def test_negative_total():
    data = {
        "invoice_number": "INV-1001",
        "invoice_date": "10/09/2026",
        "total": -500.0
    }

    result = validate_invoice(data)

    assert result["is_valid"] is False
    assert "total cannot be negative." in result["errors"]


def test_invalid_gstin():
    data = {
        "invoice_number": "INV-1001",
        "invoice_date": "10/09/2026",
        "gstin": "INVALID"
    }

    result = validate_invoice(data)

    assert result["is_valid"] is False
    assert "Invalid GSTIN format." in result["errors"]


def test_total_calculation():
    data = {
        "invoice_number": "INV-1001",
        "invoice_date": "10/09/2026",
        "subtotal": 4500.0,
        "tax": 500.0,
        "total": 6000.0
    }

    result = validate_invoice(data)

    assert result["is_valid"] is False
    assert "Subtotal + tax does not match total." in result["errors"]

def test_valid_line_item():

    line_items = [
        {
            "description": "Laptop",
            "hsn_code": "8471",
            "quantity": 2.0,
            "unit_price": 45000.0,
            "amount": 90000.0
        }
    ]

    result = validate_line_items(line_items)

    assert result == []


def test_invalid_line_item_amount():

    line_items = [
        {
            "description": "Laptop",
            "hsn_code": "8471",
            "quantity": 2.0,
            "unit_price": 45000.0,
            "amount": 95000.0
        }
    ]

    result = validate_line_items(line_items)

    assert len(result) == 1

    assert (
        "quantity × unit price does not match amount."
        in result[0]
    )


def test_line_item_with_missing_values():

    line_items = [
        {
            "description": "Laptop",
            "hsn_code": "8471",
            "quantity": None,
            "unit_price": None,
            "amount": None
        }
    ]

    result = validate_line_items(line_items)

    assert result == []