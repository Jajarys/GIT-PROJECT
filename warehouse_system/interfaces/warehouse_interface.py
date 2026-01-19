from abc import ABC, abstractmethod
from typing import List, Optional
from interfaces.product_interface import IProduct


class IWarehouse(ABC):
    @abstractmethod
    def add_product(self, product: IProduct) -> bool:
        pass

    @abstractmethod
    def remove_product(self, sku: str) -> bool:
        pass

    @abstractmethod
    def issue_product(self, sku: str, quantity: int) -> bool:
        pass

    @abstractmethod
    def receive_product(self, sku: str, quantity: int) -> bool:
        pass

    @abstractmethod
    def get_product(self, sku: str) -> Optional[IProduct]:
        pass

    @abstractmethod
    def get_all_products(self) -> List[IProduct]:
        pass

    @abstractmethod
    def inventory_check(self) -> dict:
        pass

    @abstractmethod
    def get_total_value(self) -> float:
        pass

    @abstractmethod
    def search_products(self, keyword: str) -> List[IProduct]:
        pass
