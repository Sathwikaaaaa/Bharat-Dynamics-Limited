import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

from app.database.database import Base
from app.database.models import Invoice, InvoiceItem

load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
TEST_DB_NAME = os.getenv(
    "TEST_DB_NAME",
    "invoice_test_db"
)

TEST_DATABASE_URL = (
    f"postgresql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"
)

test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True
)

Base.metadata.create_all(bind=test_engine)

print("Test database tables created successfully!")


def test_get_invoice_by_id(api_client, test_db):
    invoice = Invoice(
        invoice_number="GET-BY-ID-001",
        vendor="Test Vendor",
        customer="Test Customer",
        currency="INR",
        subtotal=1000,
        tax=180,
        total=1180
    )

    test_db.add(invoice)
    test_db.commit()
    test_db.refresh(invoice)

    response = api_client.get(
        f"/invoices/{invoice.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == invoice.id
    assert data["invoice_number"] == "GET-BY-ID-001"
    assert data["vendor"] == "Test Vendor"
    assert data["customer"] == "Test Customer"
    assert data["currency"] == "INR"
    assert data["subtotal"] == 1000.0
    assert data["tax"] == 180.0
    assert data["total"] == 1180.0
    assert data["line_items"] == []


def test_get_invoice_by_id_not_found(
    api_client
):
    response = api_client.get(
        "/invoices/999999"
    )

    assert response.status_code == 404

    data = response.json()

    assert data["detail"] == "Invoice not found."

def test_get_invoice_by_id_returns_line_items(
    api_client,
    test_db
):
    invoice = Invoice(
        invoice_number="GET-ITEM-001",
        vendor="Test Vendor",
        customer="Test Customer",
        currency="INR",
        subtotal=4000,
        tax=500,
        total=4500
    )

    test_db.add(invoice)
    test_db.commit()
    test_db.refresh(invoice)

    from app.database.models import InvoiceItem

    item = InvoiceItem(
        invoice_id=invoice.id,
        description="Laptop",
        hsn_code="8471",
        quantity=2,
        unit_price=2000,
        amount=4000
    )

    test_db.add(item)
    test_db.commit()

    response = api_client.get(
        f"/invoices/{invoice.id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data["line_items"]) == 1

    line_item = data["line_items"][0]

    assert line_item["description"] == "Laptop"
    assert line_item["hsn_code"] == "8471"
    assert line_item["quantity"] == 2.0
    assert line_item["unit_price"] == 2000.0
    assert line_item["amount"] == 4000.0