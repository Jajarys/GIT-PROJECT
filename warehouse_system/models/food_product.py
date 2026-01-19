from models.base_product import BaseProduct
from datetime import date


class FoodProduct(BaseProduct):
    def __init__(self, sku: str, name: str, price: float, quantity: int, description: str, 
                 expiration_date: date, weight: float, is_organic: bool = False):
        super().__init__(sku, name, price, quantity, "Продукти харчування", description)
        self._expiration_date = expiration_date
        self._weight = weight
        self._is_organic = is_organic

    def get_expiration_date(self) -> date:
        return self._expiration_date

    def get_weight(self) -> float:
        return self._weight

    def is_organic(self) -> bool:
        return self._is_organic

    def is_expired(self) -> bool:
        return date.today() > self._expiration_date

    def __str__(self) -> str:
        organic_status = "органічний" if self._is_organic else "звичайний"
        return f"{super().__str__()} | Термін придатності: {self._expiration_date} | {organic_status}"
