from datetime import date

from app.services.data_normalizer import normalize_invoice_date


def test_normalize_date_with_dash():
    result = normalize_invoice_date("25-10-2017")

    assert result == date(2017, 10, 25)


def test_normalize_date_with_slash():
    result = normalize_invoice_date("25/10/2017")

    assert result == date(2017, 10, 25)


def test_normalize_iso_date():
    result = normalize_invoice_date("2017-10-25")

    assert result == date(2017, 10, 25)


def test_normalize_empty_date():
    assert normalize_invoice_date("") is None


def test_normalize_invalid_date():
    assert normalize_invoice_date("invalid-date") is None


def test_already_normalized_date():
    value = date(2017, 10, 25)

    assert normalize_invoice_date(value) == value