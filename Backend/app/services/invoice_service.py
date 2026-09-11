from app.processors.image_processor import process_image
from app.processors.pdf_processor import process_pdf
from app.repositories.invoice_repository import create_invoice
from app.services.invoice_validator import validate_invoice
from app.utils.logger import get_logger


logger = get_logger(__name__)


def process_invoice_file(
    file_path: str,
    extension: str,
    db
):
    """
    Process an invoice file, validate extracted data,
    and persist valid invoices.
    """

    logger.info(
        "Starting invoice processing: %s",
        file_path
    )

    if extension == ".pdf":
        data = process_pdf(file_path)
    else:
        data = process_image(file_path)

    for invoice in data:

        invoice["validation"] = validate_invoice(
            invoice
        )

        if invoice["validation"]["is_valid"]:

            create_invoice(
                db,
                invoice
            )

    logger.info(
        "Invoice processing completed: %s",
        file_path
    )

    return data