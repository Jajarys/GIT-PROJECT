from typing import List, Optional, Dict
from interfaces.warehouse_interface import IWarehouse
from interfaces.product_interface import IProduct


class Warehouse(IWarehouse):
    def __init__(self, name: str, location: str):
        self._name = name
        self._location = location
        self._products: Dict[str, IProduct] = {}

    def get_name(self) -> str:
        return self._name

    def get_location(self) -> str:
        return self._location

    def add_product(self, product: IProduct) -> bool:
        sku = product.get_sku()
        if sku in self._products:
            existing = self._products[sku]
            existing.set_quantity(existing.get_quantity() + product.get_quantity())
            return True
        self._products[sku] = product
        return True

    def remove_product(self, sku: str) -> bool:
        if sku in self._products:
            del self._products[sku]
            return True
        return False

    def issue_product(self, sku: str, quantity: int) -> bool:
        if sku not in self._products:
            return False
        product = self._products[sku]
        if product.get_quantity() < quantity:
            return False
        product.set_quantity(product.get_quantity() - quantity)
        if product.get_quantity() == 0:
            del self._products[sku]
        return True

    def receive_product(self, sku: str, quantity: int) -> bool:
        if sku not in self._products:
            return False
        product = self._products[sku]
        product.set_quantity(product.get_quantity() + quantity)
        return True

    def get_product(self, sku: str) -> Optional[IProduct]:
        return self._products.get(sku)

    def get_all_products(self) -> List[IProduct]:
        return list(self._products.values())

    def inventory_check(self) -> dict:
        result = {
            "назва_складу": self._name,
            "локація": self._location,
            "загальна_кількість_товарів": len(self._products),
            "загальна_кількість_одиниць": sum(p.get_quantity() for p in self._products.values()),
            "загальна_вартість": self.get_total_value(),
            "категорії": {}
        }
        for product in self._products.values():
            category = product.get_category()
            if category not in result["категорії"]:
                result["категорії"][category] = {"кількість_товарів": 0, "кількість_одиниць": 0, "вартість": 0}
            result["категорії"][category]["кількість_товарів"] += 1
            result["категорії"][category]["кількість_одиниць"] += product.get_quantity()
            result["категорії"][category]["вартість"] += product.get_price() * product.get_quantity()
        return result

    def get_total_value(self) -> float:
        return sum(p.get_price() * p.get_quantity() for p in self._products.values())

    def search_products(self, keyword: str) -> List[IProduct]:
        keyword_lower = keyword.lower()
        return [p for p in self._products.values() 
                if keyword_lower in p.get_name().lower() or 
                   keyword_lower in p.get_description().lower()]

    def get_products_by_category(self, category: str) -> List[IProduct]:
        return [p for p in self._products.values() if p.get_category() == category]

    def get_low_stock_products(self, threshold: int = 10) -> List[IProduct]:
        return [p for p in self._products.values() if p.get_quantity() < threshold]

    def get_categories(self) -> List[str]:
        return list(set(p.get_category() for p in self._products.values()))

    def get_product_count(self) -> int:
        return len(self._products)

    def update_product_quantity(self, sku: str, quantity: int) -> bool:
        if sku in self._products:
            self._products[sku].set_quantity(quantity)
            return True
        return False
