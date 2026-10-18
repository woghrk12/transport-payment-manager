from datetime import date

from models.transport_record import TransportRecord


def test_transport_record_creation():
    record = TransportRecord(
        sheet_name="2026.10",
        row_number=2,
        work_date=date(2026, 10, 3),
        company="대한운수",
        name="김철수",
        departure="서울",
        destination="부산",
        amount=300000,
        note="",
        payment_date=None,
    )

    assert record.sheet_name == "2026.10"
    assert record.row_number == 2
    assert record.company == "대한운수"
    assert record.amount == 300000
    assert record.payment_date is None
