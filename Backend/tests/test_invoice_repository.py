from unittest.mock import MagicMock

from app.repositories.invoice_repository import create_invoice
import pytest

from app.repositories.invoice_repository import create_invoice

def test_create_invoice_with_line_items():
    db = MagicMock()

    invoice_data = {
        "invoice_number": "INV-1001",
        "invoice_date": "10/09/2026",
        "vendor": "ABC Technologies",
        "customer": "Bharat Dynamics Limited",
        "po_number": "PO-123",
        "gstin": "07PDUJS4678K1Z4",
        "currency": "INR",
        "subtotal": 4500.0,
        "tax": 500.0,
        "total": 5000.0,
        "raw_text": "Invoice No: INV-1001",
        "line_items": [
            {
                "description": "Laptop",
                "hsn_code": "8471",
                "quantity": 2,
                "unit_price": 2000.0,
                "amount": 4000.0
            },
            {
                "description": "Mouse",
                "hsn_code": "8471",
                "quantity": 1,
                "unit_price": 500.0,
                "amount": 500.0
            }
        ]
    }

    result = create_invoice(db, invoice_data)

    db.add.assert_called()
    db.flush.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(result)

    assert result.invoice_number == "INV-1001"
    assert result.vendor == "ABC Technologies"
    assert result.total == 5000.0

def test_create_invoice_rolls_back_on_failure():
    db = MagicMock()

    db.flush.side_effect = Exception("Database failure")

    invoice_data = {
        "invoice_number": "INV-FAIL-001",
        "invoice_date": "10/09/2026",
        "vendor": "ABC Technologies",
        "total": 5000.0
    }

    with pytest.raises(Exception, match="Database failure"):
        create_invoice(db, invoice_data)

    db.rollback.assert_called_once()
    db.commit.assert_not_called()