from sqlalchemy.orm import Session

from app.database.models import Invoice, InvoiceItem
from app.services.data_normalizer import normalize_invoice_date


def create_invoice(db: Session, invoice_data: dict):
    try:
        invoice = Invoice(
            invoice_number=invoice_data.get("invoice_number"),
            invoice_date=normalize_invoice_date(
                invoice_data.get("invoice_date")
            ),
            vendor=invoice_data.get("vendor"),
            customer=invoice_data.get("customer"),
            po_number=invoice_data.get("po_number"),
            gstin=invoice_data.get("gstin"),
            currency=invoice_data.get("currency"),
            subtotal=invoice_data.get("subtotal"),
            tax=invoice_data.get("tax"),
            total=invoice_data.get("total"),
            raw_text=invoice_data.get("raw_text")
        )

        db.add(invoice)
        db.flush()

        for item_data in invoice_data.get("line_items", []):
            item = InvoiceItem(
                invoice_id=invoice.id,
                description=item_data.get("description"),
                hsn_code=item_data.get("hsn_code"),
                quantity=item_data.get("quantity"),
                unit_price=item_data.get("unit_price"),
                amount=item_data.get("amount")
            )

            db.add(item)

        db.commit()
        db.refresh(invoice)

        return invoice

    except Exception:
        db.rollback()
        raise
def get_invoices(db: Session):
    return (
        db.query(Invoice)
        .order_by(Invoice.id.desc())
        .all()
    )
def get_invoice_by_id(
    db: Session,
    invoice_id: int
):
    return (
        db.query(Invoice)
        .filter(Invoice.id == invoice_id)
        .first()
    )