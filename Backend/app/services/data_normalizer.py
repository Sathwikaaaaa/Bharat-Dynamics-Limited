from datetime import datetime, date

from app.utils.logger import get_logger

logger = get_logger(__name__)


SUPPORTED_DATE_FORMATS = [
    "%d-%m-%Y",
    "%d/%m/%Y",
    "%Y-%m-%d",
    "%d.%m.%Y",
]


def normalize_invoice_date(value):
    if not value:
        return None

    if isinstance(value, date):
        return value

    value = value.strip()

    for date_format in SUPPORTED_DATE_FORMATS:
        try:
            return datetime.strptime(
                value,
                date_format
            ).date()
        except ValueError:
            continue

    logger.warning(
        "Unable to normalize invoice date: %s",
        value
    )

    return None