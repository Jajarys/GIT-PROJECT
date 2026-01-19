from datetime import datetime
from typing import List
from interfaces.report_interface import IReport
from interfaces.warehouse_interface import IWarehouse


class InventoryReport(IReport):
    def __init__(self, warehouse: IWarehouse):
        self._warehouse = warehouse
        self._generated_date = None
        self._report_data = None

    def generate(self) -> str:
        self._generated_date = datetime.now()
        inventory = self._warehouse.inventory_check()
        self._report_data = inventory
        
        lines = []
        lines.append("=" * 60)
        lines.append("ЗВІТ ІНВЕНТАРИЗАЦІЇ СКЛАДУ")
        lines.append("=" * 60)
        lines.append(f"Дата генерації: {self._generated_date.strftime('%d.%m.%Y %H:%M:%S')}")
        lines.append(f"Назва складу: {inventory['назва_складу']}")
        lines.append(f"Локація: {inventory['локація']}")
        lines.append("-" * 60)
        lines.append(f"Загальна кількість товарів: {inventory['загальна_кількість_товарів']}")
        lines.append(f"Загальна кількість одиниць: {inventory['загальна_кількість_одиниць']}")
        lines.append(f"Загальна вартість: {inventory['загальна_вартість']:.2f} грн.")
        lines.append("-" * 60)
        lines.append("РОЗПОДІЛ ЗА КАТЕГОРІЯМИ:")
        
        for category, data in inventory['категорії'].items():
            lines.append(f"  {category}:")
            lines.append(f"    - Кількість товарів: {data['кількість_товарів']}")
            lines.append(f"    - Кількість одиниць: {data['кількість_одиниць']}")
            lines.append(f"    - Вартість: {data['вартість']:.2f} грн.")
        
        lines.append("=" * 60)
        return "\n".join(lines)

    def get_report_type(self) -> str:
        return "Інвентаризація"

    def get_generated_date(self) -> datetime:
        return self._generated_date

    def export_to_dict(self) -> dict:
        return {
            "тип_звіту": self.get_report_type(),
            "дата_генерації": self._generated_date.isoformat() if self._generated_date else None,
            "дані": self._report_data
        }


class LowStockReport(IReport):
    def __init__(self, warehouse: IWarehouse, threshold: int = 10):
        self._warehouse = warehouse
        self._threshold = threshold
        self._generated_date = None
        self._report_data = None

    def generate(self) -> str:
        self._generated_date = datetime.now()
        low_stock_products = self._warehouse.get_low_stock_products(self._threshold)
        
        self._report_data = {
            "поріг": self._threshold,
            "товари": [
                {
                    "sku": p.get_sku(),
                    "назва": p.get_name(),
                    "кількість": p.get_quantity(),
                    "категорія": p.get_category()
                }
                for p in low_stock_products
            ]
        }
        
        lines = []
        lines.append("=" * 60)
        lines.append("ЗВІТ ПРО ТОВАРИ З НИЗЬКИМ ЗАПАСОМ")
        lines.append("=" * 60)
        lines.append(f"Дата генерації: {self._generated_date.strftime('%d.%m.%Y %H:%M:%S')}")
        lines.append(f"Поріг низького запасу: {self._threshold} одиниць")
        lines.append("-" * 60)
        
        if not low_stock_products:
            lines.append("Товарів з низьким запасом не знайдено.")
        else:
            lines.append(f"Знайдено товарів: {len(low_stock_products)}")
            lines.append("-" * 60)
            for product in low_stock_products:
                lines.append(f"SKU: {product.get_sku()}")
                lines.append(f"  Назва: {product.get_name()}")
                lines.append(f"  Кількість: {product.get_quantity()}")
                lines.append(f"  Категорія: {product.get_category()}")
                lines.append("-" * 30)
        
        lines.append("=" * 60)
        return "\n".join(lines)

    def get_report_type(self) -> str:
        return "Низький запас"

    def get_generated_date(self) -> datetime:
        return self._generated_date

    def export_to_dict(self) -> dict:
        return {
            "тип_звіту": self.get_report_type(),
            "дата_генерації": self._generated_date.isoformat() if self._generated_date else None,
            "дані": self._report_data
        }


class SalesReport(IReport):
    def __init__(self, orders: List, warehouse: IWarehouse):
        self._orders = orders
        self._warehouse = warehouse
        self._generated_date = None
        self._report_data = None

    def generate(self) -> str:
        self._generated_date = datetime.now()
        
        total_orders = len(self._orders)
        total_revenue = sum(order.get_total_amount() for order in self._orders)
        status_counts = {}
        
        for order in self._orders:
            status = order.get_status()
            status_counts[status] = status_counts.get(status, 0) + 1
        
        self._report_data = {
            "загальна_кількість_замовлень": total_orders,
            "загальний_дохід": total_revenue,
            "статуси": status_counts
        }
        
        lines = []
        lines.append("=" * 60)
        lines.append("ЗВІТ ПРО ПРОДАЖІ")
        lines.append("=" * 60)
        lines.append(f"Дата генерації: {self._generated_date.strftime('%d.%m.%Y %H:%M:%S')}")
        lines.append("-" * 60)
        lines.append(f"Загальна кількість замовлень: {total_orders}")
        lines.append(f"Загальний дохід: {total_revenue:.2f} грн.")
        lines.append("-" * 60)
        lines.append("РОЗПОДІЛ ЗА СТАТУСАМИ:")
        
        for status, count in status_counts.items():
            lines.append(f"  {status}: {count} замовлень")
        
        lines.append("=" * 60)
        return "\n".join(lines)

    def get_report_type(self) -> str:
        return "Продажі"

    def get_generated_date(self) -> datetime:
        return self._generated_date

    def export_to_dict(self) -> dict:
        return {
            "тип_звіту": self.get_report_type(),
            "дата_генерації": self._generated_date.isoformat() if self._generated_date else None,
            "дані": self._report_data
        }
