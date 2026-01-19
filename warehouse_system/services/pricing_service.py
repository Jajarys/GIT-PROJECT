from typing import Dict, Optional
from datetime import datetime


class DiscountType:
    PERCENTAGE = "percentage"
    FIXED = "fixed"


class Discount:
    def __init__(self, discount_id: str, name: str, discount_type: str, 
                 value: float, min_quantity: int = 1, max_uses: int = -1):
        self._id = discount_id
        self._name = name
        self._type = discount_type
        self._value = value
        self._min_quantity = min_quantity
        self._max_uses = max_uses
        self._uses_count = 0
        self._is_active = True
        self._created_at = datetime.now()

    def get_id(self) -> str:
        return self._id

    def get_name(self) -> str:
        return self._name

    def get_type(self) -> str:
        return self._type

    def get_value(self) -> float:
        return self._value

    def get_min_quantity(self) -> int:
        return self._min_quantity

    def is_active(self) -> bool:
        if not self._is_active:
            return False
        if self._max_uses > 0 and self._uses_count >= self._max_uses:
            return False
        return True

    def apply(self, price: float, quantity: int) -> float:
        if not self.is_active():
            return price * quantity
        
        if quantity < self._min_quantity:
            return price * quantity
        
        total = price * quantity
        
        if self._type == DiscountType.PERCENTAGE:
            discount = total * (self._value / 100)
        else:
            discount = self._value
        
        self._uses_count += 1
        return max(0, total - discount)

    def deactivate(self):
        self._is_active = False

    def activate(self):
        self._is_active = True

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "name": self._name,
            "type": self._type,
            "value": self._value,
            "min_quantity": self._min_quantity,
            "max_uses": self._max_uses,
            "uses_count": self._uses_count,
            "is_active": self._is_active
        }

    def __str__(self) -> str:
        if self._type == DiscountType.PERCENTAGE:
            value_str = f"{self._value}%"
        else:
            value_str = f"{self._value} грн."
        status = "✓" if self.is_active() else "✗"
        return f"{status} {self._name}: -{value_str}"


class PricingService:
    def __init__(self):
        self._discounts: Dict[str, Discount] = {}
        self._product_discounts: Dict[str, str] = {}
        self._category_discounts: Dict[str, str] = {}
        self._init_default_discounts()

    def _init_default_discounts(self):
        self.add_discount(Discount(
            "BULK10", "Оптова знижка 10%", 
            DiscountType.PERCENTAGE, 10, min_quantity=10
        ))
        self.add_discount(Discount(
            "BULK20", "Оптова знижка 20%", 
            DiscountType.PERCENTAGE, 20, min_quantity=50
        ))
        self.add_discount(Discount(
            "NEWYEAR", "Новорічна знижка", 
            DiscountType.PERCENTAGE, 15, max_uses=100
        ))

    def add_discount(self, discount: Discount) -> bool:
        self._discounts[discount.get_id()] = discount
        return True

    def remove_discount(self, discount_id: str) -> bool:
        if discount_id in self._discounts:
            del self._discounts[discount_id]
            return True
        return False

    def get_discount(self, discount_id: str) -> Optional[Discount]:
        return self._discounts.get(discount_id)

    def get_all_discounts(self) -> list:
        return list(self._discounts.values())

    def get_active_discounts(self) -> list:
        return [d for d in self._discounts.values() if d.is_active()]

    def assign_discount_to_product(self, sku: str, discount_id: str) -> bool:
        if discount_id in self._discounts:
            self._product_discounts[sku] = discount_id
            return True
        return False

    def assign_discount_to_category(self, category: str, discount_id: str) -> bool:
        if discount_id in self._discounts:
            self._category_discounts[category] = discount_id
            return True
        return False

    def calculate_price(self, product, quantity: int, discount_code: str = None) -> dict:
        base_price = product.get_price()
        total_base = base_price * quantity
        
        discount_applied = None
        final_price = total_base
        
        if discount_code and discount_code in self._discounts:
            discount = self._discounts[discount_code]
            if discount.is_active():
                final_price = discount.apply(base_price, quantity)
                discount_applied = discount.get_name()
        
        elif product.get_sku() in self._product_discounts:
            discount_id = self._product_discounts[product.get_sku()]
            discount = self._discounts.get(discount_id)
            if discount and discount.is_active():
                final_price = discount.apply(base_price, quantity)
                discount_applied = discount.get_name()
        
        elif product.get_category() in self._category_discounts:
            discount_id = self._category_discounts[product.get_category()]
            discount = self._discounts.get(discount_id)
            if discount and discount.is_active():
                final_price = discount.apply(base_price, quantity)
                discount_applied = discount.get_name()

        return {
            "sku": product.get_sku(),
            "name": product.get_name(),
            "quantity": quantity,
            "base_price": base_price,
            "total_base": total_base,
            "final_price": final_price,
            "discount_applied": discount_applied,
            "savings": total_base - final_price
        }

    def create_custom_discount(self, name: str, discount_type: str, 
                                value: float, min_quantity: int = 1) -> Discount:
        discount_id = f"CUSTOM_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        discount = Discount(discount_id, name, discount_type, value, min_quantity)
        self.add_discount(discount)
        return discount
