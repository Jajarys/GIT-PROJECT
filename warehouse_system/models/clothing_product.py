from models.base_product import BaseProduct


class ClothingProduct(BaseProduct):
    def __init__(self, sku: str, name: str, price: float, quantity: int, description: str,
                 size: str, color: str, material: str, gender: str):
        super().__init__(sku, name, price, quantity, "Одяг", description)
        self._size = size
        self._color = color
        self._material = material
        self._gender = gender

    def get_size(self) -> str:
        return self._size

    def get_color(self) -> str:
        return self._color

    def get_material(self) -> str:
        return self._material

    def get_gender(self) -> str:
        return self._gender

    def __str__(self) -> str:
        return f"{super().__str__()} | Розмір: {self._size} | Колір: {self._color}"
