from app.database.models import Invoice


def test_invoice_model():

    assert Invoice.__tablename__ == "invoices"

    assert Invoice.id.primary_key is True

    assert "invoice_number" in Invoice.__table__.columns
    assert "invoice_date" in Invoice.__table__.columns
    assert "vendor" in Invoice.__table__.columns
    assert "customer" in Invoice.__table__.columns
    assert "gstin" in Invoice.__table__.columns
    assert "total" in Invoice.__table__.columns