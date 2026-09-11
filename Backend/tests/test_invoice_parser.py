from app.services.invoice_parser import parse_invoice_text
from app.services.line_item_parser import parse_line_item

def test_invoice_number_extraction():

    text = """
    Invoice No: INV-1001
    Date: 10/09/2026
    Total: 5000
    """

    result = parse_invoice_text(text)

    assert result["invoice_number"] == "INV-1001"


def test_order_number_extraction():

    text = """
    Invoice No: INV-1001
    Order No: ORD-500
    Total: 5000
    """

    result = parse_invoice_text(text)

    assert result["order_number"] == "ORD-500"


def test_date_extraction():

    text = """
    Invoice No: INV-1001
    Date: 10/09/2026
    """

    result = parse_invoice_text(text)

    assert result["invoice_date"] == "10/09/2026"


def test_total_extraction():

    text = """
    Invoice No: INV-1001
    Total: 5000
    """

    result = parse_invoice_text(text)

    assert result["total"] == 5000.0


def test_subtotal_extraction():

    text = """
    Subtotal: 4500
    Tax: 500
    Total: 5000
    """

    result = parse_invoice_text(text)

    assert result["subtotal"] == 4500.0


def test_tax_extraction():

    text = """
    Subtotal: 4500
    GST: 500
    Total: 5000
    """

    result = parse_invoice_text(text)

    assert result["tax"] == 500.0


def test_vendor_extraction():

    text = """
    Vendor: ABC Technologies
    Invoice No: INV-1001
    """

    result = parse_invoice_text(text)

    assert result["vendor"] == "ABC Technologies"


def test_customer_extraction():

    text = """
    Customer: Bharat Dynamics Limited
    Invoice No: INV-1001
    """

    result = parse_invoice_text(text)

    assert (
        result["customer"]
        == "Bharat Dynamics Limited"
    )


def test_po_number_extraction():

    text = """
    PO Number: PO-12345
    Invoice No: INV-1001
    """

    result = parse_invoice_text(text)

    assert result["po_number"] == "PO-12345"


def test_currency_extraction():

    text = """
    Invoice No: INV-1001
    Total: ₹5000
    """

    result = parse_invoice_text(text)

    assert result["currency"] == "INR"


def test_raw_text_is_preserved():

    text = """
    Invoice No: INV-1001
    Total: 5000
    """

    result = parse_invoice_text(text)

    assert result["raw_text"] == text


def test_missing_fields_return_none():

    text = """
    Invoice No: INV-1001
    """

    result = parse_invoice_text(text)

    assert result["invoice_number"] == "INV-1001"

    assert result["vendor"] is None

    assert result["customer"] is None

    assert result["po_number"] is None

    assert result["subtotal"] is None

    assert result["tax"] is None

    assert result["total"] is None
def test_invoice_item_schema():
    from app.schemas.invoice_schema import InvoiceItem

    item = InvoiceItem(
        description="Computer Hardware",
        hsn_code="8471",
        quantity=2,
        unit_price=1500,
        amount=3000
    )

    assert item.description == "Computer Hardware"
    assert item.hsn_code == "8471"
    assert item.quantity == 2
    assert item.unit_price == 1500
    assert item.amount == 3000
def test_line_item_extraction():
    line = "Laptop 8471 2 45000 90000"

    result = parse_line_item(line)

    assert result["description"] == "Laptop"
    assert result["hsn_code"] == "8471"
    assert result["quantity"] == 2.0
    assert result["unit_price"] == 45000.0
    assert result["amount"] == 90000.0


def test_invalid_line_item():
    line = "Description only"

    result = parse_line_item(line)

    assert result is None
def test_line_items_are_extracted_from_invoice_text():
    text = """
    Invoice No: INV-1001

    Description HSN Qty Rate Amount
    Laptop 8471 2 45000 90000
    Mouse 8471 3 500 1500

    Subtotal: 91500
    GST: 16470
    Total: 107970
    """

    result = parse_invoice_text(text)

    assert len(result["line_items"]) == 2

    assert result["line_items"][0]["description"] == "Laptop"
    assert result["line_items"][0]["hsn_code"] == "8471"
    assert result["line_items"][0]["quantity"] == 2.0
    assert result["line_items"][0]["unit_price"] == 45000.0
    assert result["line_items"][0]["amount"] == 90000.0

    assert result["line_items"][1]["description"] == "Mouse"
    assert result["line_items"][1]["amount"] == 1500.0