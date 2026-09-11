from unittest.mock import patch

from app.services.invoice_service import process_invoice_file


@patch("app.services.invoice_service.create_invoice")
@patch("app.services.invoice_service.validate_invoice")
@patch("app.services.invoice_service.process_image")
def test_process_invoice_file_image(
    mock_process_image,
    mock_validate_invoice,
    mock_create_invoice
):
    invoice_data = [
        {
            "invoice_number": "SERVICE-001",
            "total": 5000.0
        }
    ]

    mock_process_image.return_value = invoice_data

    mock_validate_invoice.return_value = {
        "is_valid": True,
        "errors": []
    }

    fake_db = object()

    result = process_invoice_file(
        "test.jpg",
        ".jpg",
        fake_db
    )

    assert result == invoice_data

    mock_process_image.assert_called_once_with(
        "test.jpg"
    )

    mock_validate_invoice.assert_called_once_with(
        invoice_data[0]
    )

    mock_create_invoice.assert_called_once_with(
        fake_db,
        invoice_data[0]
    )


@patch("app.services.invoice_service.create_invoice")
@patch("app.services.invoice_service.validate_invoice")
@patch("app.services.invoice_service.process_image")
def test_process_invoice_file_invalid_invoice_not_saved(
    mock_process_image,
    mock_validate_invoice,
    mock_create_invoice
):
    invoice_data = [
        {
            "invoice_number": "SERVICE-INVALID",
            "total": 5000.0
        }
    ]

    mock_process_image.return_value = invoice_data

    mock_validate_invoice.return_value = {
        "is_valid": False,
        "errors": [
            "Invoice number is missing."
        ]
    }

    fake_db = object()

    result = process_invoice_file(
        "test.jpg",
        ".jpg",
        fake_db
    )

    assert result == invoice_data

    mock_validate_invoice.assert_called_once_with(
        invoice_data[0]
    )

    mock_create_invoice.assert_not_called()


@patch("app.services.invoice_service.create_invoice")
@patch("app.services.invoice_service.validate_invoice")
@patch("app.services.invoice_service.process_pdf")
def test_process_invoice_file_pdf(
    mock_process_pdf,
    mock_validate_invoice,
    mock_create_invoice
):
    invoice_data = [
        {
            "invoice_number": "SERVICE-PDF-001",
            "total": 7500.0
        }
    ]

    mock_process_pdf.return_value = invoice_data

    mock_validate_invoice.return_value = {
        "is_valid": True,
        "errors": []
    }

    fake_db = object()

    result = process_invoice_file(
        "test.pdf",
        ".pdf",
        fake_db
    )

    assert result == invoice_data

    mock_process_pdf.assert_called_once_with(
        "test.pdf"
    )

    mock_validate_invoice.assert_called_once_with(
        invoice_data[0]
    )

    mock_create_invoice.assert_called_once_with(
        fake_db,
        invoice_data[0]
    )