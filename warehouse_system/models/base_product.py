from interfaces.product_interface import IProduct


class BaseProduct(IProduct):
    def __init__(self, sku: str, name: str, price: float, quantity: int, category: str, description: str):
        self._sku = sku
        self._name = name
        self._price = price
        self._quantity = quantity
        self._category = category
        self._description = description

    def get_name(self) -> str:
        return self._name

    def get_price(self) -> float:
        return self._price

    def get_quantity(self) -> int:
        return self._quantity

    def set_quantity(self, quantity: int) -> None:
        if quantity >= 0:
            self._quantity = quantity

    def get_category(self) -> str:
        return self._category

    def get_description(self) -> str:
        return self._description

    def get_sku(self) -> str:
        return self._sku

    def __str__(self) -> str:
        return f"{self._name} (SKU: {self._sku}) - {self._quantity} шт. по {self._price} грн."
