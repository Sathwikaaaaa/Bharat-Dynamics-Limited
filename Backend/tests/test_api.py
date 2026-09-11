from io import BytesIO
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.api.app import app
from app.database.models import Invoice
from app.api.app import app
from app.database.database import get_db
from app.database.models import Invoice
from io import BytesIO
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.api.app import app
from app.database.database import get_db
from app.database.models import Invoice


client = TestClient(app)
@pytest.fixture
def api_client(test_db):

    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db

    yield client

    app.dependency_overrides.clear()

def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }


@patch(
    "app.services.invoice_service.process_image"
)
def test_upload_image(mock_process_image):
    mock_process_image.return_value = [
        {
            "invoice_number": "INV-1001",
            "total": 5000.0
        }
    ]

    response = client.post(
        "/invoices/upload",
        files={
            "file": (
                "invoice.jpg",
                BytesIO(b"fake image"),
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["filename"] == "invoice.jpg"

    assert data["status"] == "processed"

    assert isinstance(
        data["data"],
        list
    )

    assert (
        data["data"][0]["invoice_number"]
        == "INV-1001"
    )

    assert (
        data["data"][0]["total"]
        == 5000.0
    )


@patch(
    "app.services.invoice_service.process_image"
)
def test_upload_image_contains_validation(
    mock_process_image
):
    mock_process_image.return_value = [
        {
            "invoice_number": "INV-1001",
            "invoice_date": "10/09/2026",
            "gstin": "07PDUJS4678K1Z4",
            "subtotal": 4500.0,
            "tax": 500.0,
            "total": 5000.0,
            "line_items": [],
            "raw_text": "Invoice No: INV-1001"
        }
    ]

    response = client.post(
        "/invoices/upload",
        files={
            "file": (
                "invoice.jpg",
                BytesIO(b"fake image"),
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "validation" in data["data"][0]

    assert (
        data["data"][0]["validation"]["is_valid"]
        is True
    )

    assert (
        data["data"][0]["validation"]["errors"]
        == []
    )


def test_upload_invoice_persists_to_database(
    monkeypatch,
    test_db
):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    invoice_data = [
        {
            "invoice_number": "TEST-DB-001",
            "invoice_date": "10/09/2026",
            "vendor": "ABC Technologies",
            "customer": "Bharat Dynamics Limited",
            "po_number": "PO-001",
            "gstin": "07PDUJS4678K1Z4",
            "currency": "INR",
            "subtotal": 4500.0,
            "tax": 500.0,
            "total": 5000.0,
            "line_items": [],
            "raw_text": "Invoice No: TEST-DB-001"
        }
    ]


    monkeypatch.setattr(
    "app.services.invoice_service.process_image",
    lambda _: invoice_data
)

    response = client.post(
        "/invoices/upload",
        files={
            "file": (
                "test.jpg",
                b"fake image content",
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 200

    db = test_db

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.invoice_number == "TEST-DB-001"
        )
        .first()
    )

    assert invoice is not None

    assert invoice.vendor == "ABC Technologies"

    assert invoice.customer == "Bharat Dynamics Limited"

    assert invoice.total == 5000
   

    app.dependency_overrides.clear()


def test_upload_invoice_persists_line_items(
    monkeypatch,
    test_db
):
    def override_get_db():
        yield test_db

    app.dependency_overrides[get_db] = override_get_db
    invoice_data = [
        {
            "invoice_number": "TEST-ITEM-001",
            "invoice_date": "10/09/2026",
            "vendor": "ABC Technologies",
            "customer": "Bharat Dynamics Limited",
            "po_number": "PO-002",
            "gstin": "07PDUJS4678K1Z4",
            "currency": "INR",
            "subtotal": 4000.0,
            "tax": 500.0,
            "total": 4500.0,
            "line_items": [
                {
                    "description": "Laptop",
                    "hsn_code": "8471",
                    "quantity": 2,
                    "unit_price": 2000.0,
                    "amount": 4000.0
                }
            ],
            "raw_text": "Invoice No: TEST-ITEM-001"
        }
    ]

    monkeypatch.setattr(
    "app.services.invoice_service.process_image",
    lambda _: invoice_data
)

    response = client.post(
        "/invoices/upload",
        files={
            "file": (
                "test.jpg",
                b"fake image content",
                "image/jpeg"
            )
        }
    )

    assert response.status_code == 200

    db = test_db

    invoice = (
        db.query(Invoice)
        .filter(
            Invoice.invoice_number == "TEST-ITEM-001"
        )
        .first()
    )

    assert invoice is not None

    assert len(invoice.items) == 1

    item = invoice.items[0]

    assert item.description == "Laptop"

    assert item.hsn_code == "8471"

    assert item.quantity == 2

    assert item.unit_price == 2000

    assert item.amount == 4000
    app.dependency_overrides.clear()

def test_list_invoices(api_client, test_db):
    response = api_client.get("/invoices")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)
def test_list_invoices_returns_stored_invoice(
    api_client,
    test_db
):
    invoice = Invoice(
        invoice_number="GET-TEST-001",
        vendor="Test Vendor",
        customer="Test Customer",
        currency="INR",
        subtotal=1000,
        tax=180,
        total=1180
    )

    test_db.add(invoice)
    test_db.commit()

    response = api_client.get("/invoices")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1

    assert data[0]["invoice_number"] == "GET-TEST-001"
    assert data[0]["vendor"] == "Test Vendor"
    assert data[0]["customer"] == "Test Customer"
    assert data[0]["currency"] == "INR"
    assert data[0]["subtotal"] == 1000.0
    assert data[0]["tax"] == 180.0
    assert data[0]["total"] == 1180.0