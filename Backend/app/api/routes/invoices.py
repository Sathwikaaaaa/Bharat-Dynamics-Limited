import os
import shutil
import tempfile
import uuid
from app.schemas.invoice_schema import JobStatusResponse
from app.repositories.job_repository import get_job
from app.queue.queue_manager import queue_service
from app.repositories.job_repository import create_job
from fastapi import (
    APIRouter,
    Depends,
    File,
    HTTPException,
    UploadFile
)
from sqlalchemy.orm import Session

from app.api.dependencies.auth_dependencies import get_current_user
from app.database.database import get_db
from app.database.models import User
from app.repositories.invoice_repository import (
    get_invoices,
    get_invoice_by_id
)
from app.schemas.invoice_schema import (
    InvoiceUploadResponse,
    InvoiceItem,
    InvoiceListItem,
    InvoiceDetailResponse
)
from app.services.invoice_service import process_invoice_file
from app.storage.storage_factory import get_storage
from app.utils.logger import get_logger


router = APIRouter(
    prefix="/invoices",
    tags=["Invoices"]
)

logger = get_logger(__name__)

ALLOWED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".pdf"
}

storage = get_storage()

@router.post("/upload")
async def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )

    temporary_path = None

    try:
        # 1. Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            temporary_path = temp_file.name

            shutil.copyfileobj(
                file.file,
                temp_file
            )

        logger.info(
            "Invoice uploaded: %s",
            file.filename
        )

        # 2. Store file in S3/local storage
        stored_path = storage.save(
            temporary_path,
            file.filename
        )

        logger.info(
            "Invoice stored at: %s",
            stored_path
        )

        # 3. Generate unique job ID
        job_id = str(uuid.uuid4())

        # 4. Create job in PostgreSQL
        job = create_job(
            db=db,
            job_id=job_id,
            file_name=file.filename,
            file_path=file.filename
        )

        # 5. Add job to queue
        queue_service.enqueue({
            "job_id": job_id,
            "file_name": file.filename,
            "file_path": file.filename,
            "extension": extension
        })

        logger.info(
            "Invoice job queued: %s",
            job_id
        )

        return {
            "job_id": job.job_id,
            "filename": file.filename,
            "status": "queued"
        }

    except Exception:
        logger.exception(
            "Invoice upload failed: %s",
            file.filename
        )

        raise HTTPException(
            status_code=500,
            detail="Invoice upload failed."
        )

    finally:
        # Temporary upload can be deleted because
        # the permanent copy is already in storage.
        if (
            temporary_path
            and os.path.exists(temporary_path)
        ):
            os.remove(temporary_path)

@router.get(
    "",
    response_model=list[InvoiceListItem]
)
def list_invoices(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info("Fetching stored invoices")

    invoices = get_invoices(db)

    return [
        InvoiceListItem(
            id=invoice.id,
            invoice_number=invoice.invoice_number,
            invoice_date=(
                invoice.invoice_date.isoformat()
                if invoice.invoice_date
                else None
            ),
            vendor=invoice.vendor,
            customer=invoice.customer,
            po_number=invoice.po_number,
            gstin=invoice.gstin,
            currency=invoice.currency,
            subtotal=(
                float(invoice.subtotal)
                if invoice.subtotal is not None
                else None
            ),
            tax=(
                float(invoice.tax)
                if invoice.tax is not None
                else None
            ),
            total=(
                float(invoice.total)
                if invoice.total is not None
                else None
            )
        )
        for invoice in invoices
    ]


@router.get(
    "/{invoice_id}",
    response_model=InvoiceDetailResponse
)
def get_invoice(
    invoice_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logger.info(
        "Fetching invoice with ID: %s",
        invoice_id
    )

    invoice = get_invoice_by_id(
        db,
        invoice_id
    )

    if invoice is None:

        logger.warning(
            "Invoice not found: %s",
            invoice_id
        )

        raise HTTPException(
            status_code=404,
            detail="Invoice not found."
        )

    return InvoiceDetailResponse(
        id=invoice.id,
        invoice_number=invoice.invoice_number,
        invoice_date=(
            invoice.invoice_date.isoformat()
            if invoice.invoice_date
            else None
        ),
        vendor=invoice.vendor,
        customer=invoice.customer,
        po_number=invoice.po_number,
        gstin=invoice.gstin,
        currency=invoice.currency,
        subtotal=(
            float(invoice.subtotal)
            if invoice.subtotal is not None
            else None
        ),
        tax=(
            float(invoice.tax)
            if invoice.tax is not None
            else None
        ),
        total=(
            float(invoice.total)
            if invoice.total is not None
            else None
        ),
        line_items=[
            InvoiceItem(
                description=item.description,
                hsn_code=item.hsn_code,
                quantity=(
                    float(item.quantity)
                    if item.quantity is not None
                    else None
                ),
                unit_price=(
                    float(item.unit_price)
                    if item.unit_price is not None
                    else None
                ),
                amount=(
                    float(item.amount)
                    if item.amount is not None
                    else None
                )
            )
            for item in invoice.items
        ]
    )
@router.get(
    "/jobs/{job_id}",
    response_model=JobStatusResponse
)
def get_job_status(
    job_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    job = get_job(db, job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return {
        "job_id": job.job_id,
        "file_name": job.file_name,
        "status": job.status,
        "error_message": job.error_message
    }