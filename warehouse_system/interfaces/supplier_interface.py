from abc import ABC, abstractmethod
from typing import List


class ISupplier(ABC):
    @abstractmethod
    def get_supplier_id(self) -> str:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_contact_info(self) -> dict:
        pass

    @abstractmethod
    def get_products_supplied(self) -> List[str]:
        pass

    @abstractmethod
    def add_product_to_catalog(self, sku: str) -> bool:
        pass

    @abstractmethod
    def remove_product_from_catalog(self, sku: str) -> bool:
        pass
