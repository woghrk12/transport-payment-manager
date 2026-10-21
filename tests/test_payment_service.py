from datetime import date

import pytest

from services.payment_service import PaymentService


@pytest.mark.parametrize(
    "value, default_year, expected",
    [
        ("2026-10-19", None, date(2026, 10, 19)),
        ("20261019", None, date(2026, 10, 19)),
        ("1019", 2026, date(2026, 10, 19)),
        (" 2026-10-19", None, date(2026, 10, 19)),
        ("0229", 2028, date(2028, 2, 29)),
    ],
)
def test_parse_valid_payment_dates(value, default_year, expected):
    result = PaymentService.parse_payment_date(value, default_year)

    assert result == expected


@pytest.mark.parametrize(
    "value, default_year",
    [
        ("", 2026),
        ("2026-02-30", None),
        ("20260230", None),
        ("1332", 2026),
        ("0229", 2026),
        ("2026/10/19", None),
        ("abc", 2026),
        ("2026101", None),
        ("1019", None)
    ]
)
def test_reject_invalid_payment_date(value, default_year):
    with pytest.raises(ValueError):
        PaymentService.parse_payment_date(value, default_year)
