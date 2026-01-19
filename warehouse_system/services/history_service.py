from datetime import datetime
from typing import List, Optional
from enum import Enum


class OperationType(Enum):
    PRODUCT_ADDED = "Додано товар"
    PRODUCT_REMOVED = "Видалено товар"
    PRODUCT_ISSUED = "Видано товар"
    PRODUCT_RECEIVED = "Отримано товар"
    ORDER_CREATED = "Створено замовлення"
    ORDER_PROCESSED = "Оброблено замовлення"
    ORDER_CANCELLED = "Скасовано замовлення"
    INVENTORY_CHECK = "Інвентаризація"
    REPORT_GENERATED = "Згенеровано звіт"


class HistoryRecord:
    def __init__(self, operation_type: OperationType, description: str, 
                 user: str = "Система", details: dict = None):
        self._id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self._timestamp = datetime.now()
        self._operation_type = operation_type
        self._description = description
        self._user = user
        self._details = details or {}

    def get_id(self) -> str:
        return self._id

    def get_timestamp(self) -> datetime:
        return self._timestamp

    def get_operation_type(self) -> OperationType:
        return self._operation_type

    def get_description(self) -> str:
        return self._description

    def get_user(self) -> str:
        return self._user

    def get_details(self) -> dict:
        return self._details

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "timestamp": self._timestamp.isoformat(),
            "operation_type": self._operation_type.value,
            "description": self._description,
            "user": self._user,
            "details": self._details
        }

    def __str__(self) -> str:
        time_str = self._timestamp.strftime("%d.%m.%Y %H:%M:%S")
        return f"[{time_str}] {self._operation_type.value}: {self._description}"


class HistoryService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._records: List[HistoryRecord] = []
        return cls._instance

    def add_record(self, operation_type: OperationType, description: str,
                   user: str = "Система", details: dict = None) -> HistoryRecord:
        record = HistoryRecord(operation_type, description, user, details)
        self._records.append(record)
        return record

    def get_all_records(self) -> List[HistoryRecord]:
        return self._records.copy()

    def get_records_by_type(self, operation_type: OperationType) -> List[HistoryRecord]:
        return [r for r in self._records if r.get_operation_type() == operation_type]

    def get_records_by_date(self, date: datetime) -> List[HistoryRecord]:
        return [r for r in self._records 
                if r.get_timestamp().date() == date.date()]

    def get_recent_records(self, count: int = 10) -> List[HistoryRecord]:
        return self._records[-count:] if self._records else []

    def get_records_count(self) -> int:
        return len(self._records)

    def clear_history(self) -> None:
        self._records.clear()

    def export_to_list(self) -> List[dict]:
        return [r.to_dict() for r in self._records]

    def get_statistics(self) -> dict:
        stats = {}
        for op_type in OperationType:
            count = len([r for r in self._records if r.get_operation_type() == op_type])
            if count > 0:
                stats[op_type.value] = count
        return stats
