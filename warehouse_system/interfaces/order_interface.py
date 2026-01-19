from abc import ABC, abstractmethod
from typing import List, Tuple
from datetime import datetime


class IOrder(ABC):
    @abstractmethod
    def get_order_id(self) -> str:
        pass

    @abstractmethod
    def get_items(self) -> List[Tuple[str, int]]:
        pass

    @abstractmethod
    def add_item(self, sku: str, quantity: int) -> bool:
        pass

    @abstractmethod
    def remove_item(self, sku: str) -> bool:
        pass

    @abstractmethod
    def get_status(self) -> str:
        pass

    @abstractmethod
    def set_status(self, status: str) -> None:
        pass

    @abstractmethod
    def get_created_date(self) -> datetime:
        pass

    @abstractmethod
    def get_total_amount(self) -> float:
        pass

    @abstractmethod
    def calculate_total(self, warehouse) -> float:
        pass
