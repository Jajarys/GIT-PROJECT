from typing import List
from interfaces.supplier_interface import ISupplier


class Supplier(ISupplier):
    def __init__(self, supplier_id: str, name: str, email: str, phone: str, address: str):
        self._supplier_id = supplier_id
        self._name = name
        self._email = email
        self._phone = phone
        self._address = address
        self._products_supplied: List[str] = []

    def get_supplier_id(self) -> str:
        return self._supplier_id

    def get_name(self) -> str:
        return self._name

    def get_contact_info(self) -> dict:
        return {
            "електронна_пошта": self._email,
            "телефон": self._phone,
            "адреса": self._address
        }

    def get_products_supplied(self) -> List[str]:
        return self._products_supplied.copy()

    def add_product_to_catalog(self, sku: str) -> bool:
        if sku not in self._products_supplied:
            self._products_supplied.append(sku)
            return True
        return False

    def remove_product_from_catalog(self, sku: str) -> bool:
        if sku in self._products_supplied:
            self._products_supplied.remove(sku)
            return True
        return False

    def __str__(self) -> str:
        return f"Постачальник: {self._name} (ID: {self._supplier_id}) | Товарів: {len(self._products_supplied)}"
