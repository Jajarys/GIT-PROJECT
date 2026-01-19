from typing import List, Tuple
from datetime import datetime
from interfaces.order_interface import IOrder
from interfaces.warehouse_interface import IWarehouse
import uuid


class OrderStatus:
    PENDING = "Очікує"
    PROCESSING = "В обробці"
    SHIPPED = "Відправлено"
    DELIVERED = "Доставлено"
    CANCELLED = "Скасовано"


class Order(IOrder):
    def __init__(self, order_id: str = None):
        self._order_id = order_id or str(uuid.uuid4())[:8].upper()
        self._items: List[Tuple[str, int]] = []
        self._status = OrderStatus.PENDING
        self._created_date = datetime.now()
        self._total_amount = 0.0

    def get_order_id(self) -> str:
        return self._order_id

    def get_items(self) -> List[Tuple[str, int]]:
        return self._items.copy()

    def add_item(self, sku: str, quantity: int) -> bool:
        if quantity <= 0:
            return False
        for i, (item_sku, item_qty) in enumerate(self._items):
            if item_sku == sku:
                self._items[i] = (sku, item_qty + quantity)
                return True
        self._items.append((sku, quantity))
        return True

    def remove_item(self, sku: str) -> bool:
        for i, (item_sku, _) in enumerate(self._items):
            if item_sku == sku:
                self._items.pop(i)
                return True
        return False

    def get_status(self) -> str:
        return self._status

    def set_status(self, status: str) -> None:
        self._status = status

    def get_created_date(self) -> datetime:
        return self._created_date

    def get_total_amount(self) -> float:
        return self._total_amount

    def calculate_total(self, warehouse: IWarehouse) -> float:
        total = 0.0
        for sku, quantity in self._items:
            product = warehouse.get_product(sku)
            if product:
                total += product.get_price() * quantity
        self._total_amount = total
        return total

    def process_order(self, warehouse: IWarehouse) -> bool:
        for sku, quantity in self._items:
            product = warehouse.get_product(sku)
            if not product or product.get_quantity() < quantity:
                return False
        for sku, quantity in self._items:
            warehouse.issue_product(sku, quantity)
        self._status = OrderStatus.PROCESSING
        return True

    def __str__(self) -> str:
        return f"Замовлення #{self._order_id} | Статус: {self._status} | Сума: {self._total_amount:.2f} грн."
