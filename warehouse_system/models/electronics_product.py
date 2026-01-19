from models.base_product import BaseProduct


class ElectronicsProduct(BaseProduct):
    def __init__(self, sku: str, name: str, price: float, quantity: int, description: str,
                 brand: str, warranty_months: int, power_consumption: float):
        super().__init__(sku, name, price, quantity, "Електроніка", description)
        self._brand = brand
        self._warranty_months = warranty_months
        self._power_consumption = power_consumption

    def get_brand(self) -> str:
        return self._brand

    def get_warranty_months(self) -> int:
        return self._warranty_months

    def get_power_consumption(self) -> float:
        return self._power_consumption

    def __str__(self) -> str:
        return f"{super().__str__()} | Бренд: {self._brand} | Гарантія: {self._warranty_months} міс."
