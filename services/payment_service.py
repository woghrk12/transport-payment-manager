import re
from datetime import date


class PaymentService:
    @staticmethod
    def parse_payment_date(value: str, default_year: int | None = None) -> date:
        text = value.strip()

        if not text:
            raise ValueError("입금 날짜를 입력해야 합니다.")

        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", text):
            year, month, day = map(int, text.split("-"))

        elif re.fullmatch(r"\d{8}", text):
            year = int(text[:4])
            month = int(text[4:6])
            day = int(text[6:8])

        elif re.fullmatch(r"\d{4}", text):
            if default_year is None:
                raise ValueError("4자리 날짜 입력에는 기준 연도가 필요합니다.")

            year = default_year
            month = int(text[:2])
            day = int(text[2:4])

        else:
            raise ValueError("지원하지 않는 날짜 형식입니다. YYYY-MM-DD, YYYYMMDD, MMDD 형식을 사용하세요.")

        try:
            return date(year, month, day)
        except ValueError as error:
            raise ValueError(f"존재하지 않는 날짜입니다: {text}") from error
