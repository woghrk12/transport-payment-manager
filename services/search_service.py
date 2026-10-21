from enum import Enum

from models.transport_record import TransportRecord


class PaymentStatus(Enum):
    ALL = "all"
    UNPAID = "unpaid"
    PAID = "paid"


class SearchService:
    def search(self, records: list[TransportRecord], keyword: str = "", payment_status: PaymentStatus = PaymentStatus.ALL) -> list[TransportRecord]:
        normalized_keyword = keyword.strip().casefold()

        results = []

        for record in records:
            if not self._is_match_keyword(record, normalized_keyword):
                continue

            if not self._is_match_payment_status(record, payment_status):
                continue

            results.append(record)

        return sorted(results, key=lambda record: (record.sheet_name, record.row_number))

    @staticmethod
    def _is_match_keyword(record: TransportRecord, keyword: str) -> bool:
        if not keyword:
            return True

        return (keyword in record.company.casefold() or keyword in record.name.casefold())

    @staticmethod
    def _is_match_payment_status(record: TransportRecord, payment_status: PaymentStatus) -> bool:
        if payment_status == PaymentStatus.ALL:
            return True

        if payment_status == PaymentStatus.UNPAID:
            return record.payment_date is None

        if payment_status == PaymentStatus.PAID:
            return record.payment_date is not None

        raise ValueError(f"지원하지 않는 입금 상태입니다: {payment_status}")
