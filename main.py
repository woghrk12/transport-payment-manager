import sys

from repositories.excel_repository import ExcelRepository


def main():
    if len(sys.argv) < 2:
        print("사용법: python main.py <Excel 파일 경로>")
        return

    file_path = sys.argv[1]
    repository = ExcelRepository(file_path)

    try:
        records = repository.get_all_records()
    except (OSError, ValueError) as error:
        print(f"파일 읽기 실패: {error}")
        return

    print(f"전체 운수 기록: {len(records)}건")

    for record in records:
        print(f"[{record.sheet_name}:{record.row_number}] {record.work_date} | {record.company} | {record.name} | {record.amount:,}원 | 입금일: {record.payment_date}")


if __name__ == "__main__":
    main()
