import argparse

from repositories.excel_repository import ExcelRepository
from services.search_service import PaymentStatus, SearchService


def main():
    parser = argparse.ArgumentParser(description="운수 기록 검색 프로그램")

    parser.add_argument("file_path", help="운수 기록 Excel 파일 경로")
    parser.add_argument("--search", default="", help="검색할 회사명 또는 이름")
    parser.add_argument("--status", choices=["all", "unpaid", "paid"], default="all", help="입금 상태 필터")

    args = parser.parse_args()

    repository = ExcelRepository(args.file_path)
    search_service = SearchService()

    try:
        records = repository.get_all_records()
    except (OSError, ValueError) as error:
        parser.exit(1, f"파일 읽기 실패: {error}\n")

    results = search_service.search(records=records, keyword=args.search, payment_status=PaymentStatus(args.status))

    print(f"\n 검색 결과: {len(results)}건\n")

    for record in results:
        payment_date = (record.payment_date.isoformat() if record.payment_date else "미입금")

        print(f"[{record.sheet_name}:{record.row_number}] {record.work_date} | {record.company} | {record.name} | {record.departure} -> {record.destination} | {record.amount:,}원 | {record.payment_date}")

    total_amount = sum(record.amount for record in results)

    print(f"\n검색된 운수 금액 합계: {total_amount:,}원")


if __name__ == "__main__":
    main()
