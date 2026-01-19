from typing import Dict, List, Tuple
from datetime import datetime
from interfaces.warehouse_interface import IWarehouse


class StatisticsService:
    def __init__(self, warehouse: IWarehouse):
        self._warehouse = warehouse

    def get_category_distribution(self) -> Dict[str, int]:
        distribution = {}
        for product in self._warehouse.get_all_products():
            category = product.get_category()
            distribution[category] = distribution.get(category, 0) + 1
        return distribution

    def get_value_distribution(self) -> Dict[str, float]:
        distribution = {}
        for product in self._warehouse.get_all_products():
            category = product.get_category()
            value = product.get_price() * product.get_quantity()
            distribution[category] = distribution.get(category, 0.0) + value
        return distribution

    def get_top_products_by_value(self, count: int = 5) -> List[Tuple[str, float]]:
        products = self._warehouse.get_all_products()
        valued = [(p.get_name(), p.get_price() * p.get_quantity()) for p in products]
        valued.sort(key=lambda x: x[1], reverse=True)
        return valued[:count]

    def get_top_products_by_quantity(self, count: int = 5) -> List[Tuple[str, int]]:
        products = self._warehouse.get_all_products()
        quantified = [(p.get_name(), p.get_quantity()) for p in products]
        quantified.sort(key=lambda x: x[1], reverse=True)
        return quantified[:count]

    def get_price_range(self) -> Dict[str, float]:
        products = self._warehouse.get_all_products()
        if not products:
            return {"мінімум": 0, "максимум": 0, "середня": 0}
        prices = [p.get_price() for p in products]
        return {
            "мінімум": min(prices),
            "максимум": max(prices),
            "середня": sum(prices) / len(prices)
        }

    def get_stock_health(self) -> Dict[str, int]:
        products = self._warehouse.get_all_products()
        health = {
            "критично_низький": 0,
            "низький": 0,
            "нормальний": 0,
            "високий": 0
        }
        for p in products:
            qty = p.get_quantity()
            if qty <= 5:
                health["критично_низький"] += 1
            elif qty <= 15:
                health["низький"] += 1
            elif qty <= 50:
                health["нормальний"] += 1
            else:
                health["високий"] += 1
        return health

    def get_summary(self) -> Dict:
        products = self._warehouse.get_all_products()
        total_items = sum(p.get_quantity() for p in products)
        total_value = self._warehouse.get_total_value()
        
        return {
            "загальна_кількість_товарів": len(products),
            "загальна_кількість_одиниць": total_items,
            "загальна_вартість": total_value,
            "середня_вартість_товару": total_value / len(products) if products else 0,
            "кількість_категорій": len(self.get_category_distribution()),
            "дата_аналізу": datetime.now().strftime("%d.%m.%Y %H:%M")
        }

    def generate_ascii_chart(self, data: Dict[str, int], title: str) -> str:
        if not data:
            return "Немає даних для відображення"
        
        max_val = max(data.values()) if data.values() else 1
        max_label_len = max(len(str(k)) for k in data.keys())
        
        lines = [f"\n  {title}", "  " + "─" * 40]
        
        for label, value in data.items():
            bar_length = int((value / max_val) * 25) if max_val > 0 else 0
            bar = "█" * bar_length
            lines.append(f"  {label:<{max_label_len}} │ {bar} {value}")
        
        lines.append("  " + "─" * 40)
        return "\n".join(lines)
