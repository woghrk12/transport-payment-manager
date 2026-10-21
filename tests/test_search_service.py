from datetime import date

from models.transport_record import TransportRecord
from services.search_service import PaymentStatus, SearchService


def create_sample_records() -> list[TransportRecord]:
    return [
        TransportRecord("2026.09", 2, date(2026, 9, 20), "대한운수", "김철수", "서울", "부산", 300000, "", None),
        TransportRecord("2026.10", 2, date(2026, 10, 10), "대한운수", "김철수", "인천", "대전", 200000, "", None),
        TransportRecord("2026.10", 3, date(2026, 10, 15), "한빛물류", "이영희", "대구", "광주", "250,000", "", date(2026, 11, 14)),
        TransportRecord("2026.10", 4, date(2026, 10, 20), "대한물류", "김기태", "울산", "서울", "350,000", "", date(2026, 11, 20))
    ]


def test_search_by_company():
    service = SearchService()

    results = service.search(create_sample_records(), keyword="대한")

    assert len(results) == 3


def test_search_by_name():
    service = SearchService()

    results = service.search(create_sample_records(), keyword="철수")

    assert len(results) == 2


def test_search_unpaid_records():
    service = SearchService()

    results = service.search(create_sample_records(), keyword="대한", payment_status=PaymentStatus.UNPAID)

    assert len(results) == 2
    assert all(record.payment_date is None for record in results)


def test_search_paid_records():
    service = SearchService()

    results = service.search(create_sample_records(), payment_status=PaymentStatus.PAID)

    assert len(results) == 2
    assert all(record.payment_date is not None for record in results)


def test_search_ignores_surrounding_spaces():
    service = SearchService()

    results = service.search(create_sample_records(), keyword="     대한     ")

    assert len(results) == 3


def test_search_results_are_sorted():
    service = SearchService()

    records = list(reversed(create_sample_records()))
    results = service.search(records)

    assert [record.work_date for record in results] == sorted(record.work_date for record in results)


def test_search_does_not_modify_original_records():
    service = SearchService()

    records = create_sample_records()
    original_order = [record.row_number for record in records]

    service.search(records, keyword="대한")

    assert [record.row_number for record in records] == original_order
    assert len(records) == 4
