from abc import ABC, abstractmethod


class IProduct(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        pass

    @abstractmethod
    def get_quantity(self) -> int:
        pass

    @abstractmethod
    def set_quantity(self, quantity: int) -> None:
        pass

    @abstractmethod
    def get_category(self) -> str:
        pass

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_sku(self) -> str:
        pass
