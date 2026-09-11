from pydantic import BaseModel, Field


class InvoiceItem(BaseModel):
    description: str | None = None
    hsn_code: str | None = None
    quantity: float | None = None
    unit_price: float | None = None
    amount: float | None = None


class InvoiceValidation(BaseModel):
    is_valid: bool
    errors: list[str] = Field(default_factory=list)


class InvoiceData(BaseModel):
    invoice_number: str | None = None
    order_number: str | None = None
    invoice_date: str | None = None
    vendor: str | None = None
    customer: str | None = None
    po_number: str | None = None
    gstin: str | None = None
    currency: str | None = None
    subtotal: float | None = None
    tax: float | None = None
    total: float | None = None
    line_items: list[InvoiceItem] = Field(default_factory=list)
    raw_text: str | None = None
    validation: InvoiceValidation | None = None


class InvoiceUploadResponse(BaseModel):
    filename: str
    status: str
    data: list[InvoiceData]

class InvoiceListItem(BaseModel):
    id: int
    invoice_number: str | None = None
    invoice_date: str | None = None
    vendor: str | None = None
    customer: str | None = None
    po_number: str | None = None
    gstin: str | None = None
    currency: str | None = None
    subtotal: float | None = None
    tax: float | None = None
    total: float | None = None

class InvoiceDetailResponse(BaseModel):
    id: int
    invoice_number: str | None = None
    invoice_date: str | None = None
    vendor: str | None = None
    customer: str | None = None
    po_number: str | None = None
    gstin: str | None = None
    currency: str | None = None
    subtotal: float | None = None
    tax: float | None = None
    total: float | None = None
    line_items: list[InvoiceItem] = Field(
        default_factory=list
    )


class JobStatusResponse(BaseModel):
    job_id: str
    file_name: str
    status: str
    invoice_id: int | None = None
    error_message: str | None = None