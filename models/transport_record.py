from dataclasses import dataclass
from datetime import date


@dataclass
class TransportRecord:
    sheet_name: str
    row_number: int

    work_date: date
    company: str
    name: str
    departure: str
    destination: str
    amount: int
    note: str
    payment_date: date | None
