from models.base_product import BaseProduct


class HouseholdProduct(BaseProduct):
    def __init__(self, sku: str, name: str, price: float, quantity: int, description: str,
                 room_type: str, dimensions: dict, weight: float):
        super().__init__(sku, name, price, quantity, "Господарські товари", description)
        self._room_type = room_type
        self._dimensions = dimensions
        self._weight = weight

    def get_room_type(self) -> str:
        return self._room_type

    def get_dimensions(self) -> dict:
        return self._dimensions

    def get_weight(self) -> float:
        return self._weight

    def __str__(self) -> str:
        dims = f"{self._dimensions.get('width', 0)}x{self._dimensions.get('height', 0)}x{self._dimensions.get('depth', 0)} см"
        return f"{super().__str__()} | Кімната: {self._room_type} | Розміри: {dims}"
