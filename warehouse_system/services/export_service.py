import os
import json
import csv
from datetime import datetime
from typing import List
from interfaces.warehouse_interface import IWarehouse
from interfaces.product_interface import IProduct


class ExportService:
    def __init__(self, export_dir: str = "exports"):
        self._export_dir = export_dir
        self._ensure_export_dir()

    def _ensure_export_dir(self):
        if not os.path.exists(self._export_dir):
            os.makedirs(self._export_dir)

    def _get_filepath(self, filename: str) -> str:
        return os.path.join(self._export_dir, filename)

    def _generate_filename(self, prefix: str, extension: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{prefix}_{timestamp}.{extension}"

    def export_products_to_csv(self, warehouse: IWarehouse) -> str:
        filename = self._generate_filename("products", "csv")
        filepath = self._get_filepath(filename)
        
        products = warehouse.get_all_products()
        
        with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')
            writer.writerow(['SKU', 'Назва', 'Категорія', 'Кількість', 'Ціна', 'Вартість', 'Опис'])
            
            for p in products:
                writer.writerow([
                    p.get_sku(),
                    p.get_name(),
                    p.get_category(),
                    p.get_quantity(),
                    p.get_price(),
                    p.get_price() * p.get_quantity(),
                    p.get_description()
                ])
        
        return filepath

    def export_products_to_json(self, warehouse: IWarehouse) -> str:
        filename = self._generate_filename("products", "json")
        filepath = self._get_filepath(filename)
        
        products = warehouse.get_all_products()
        data = {
            "export_date": datetime.now().isoformat(),
            "total_products": len(products),
            "total_value": warehouse.get_total_value(),
            "products": []
        }
        
        for p in products:
            data["products"].append({
                "sku": p.get_sku(),
                "name": p.get_name(),
                "category": p.get_category(),
                "quantity": p.get_quantity(),
                "price": p.get_price(),
                "total_value": p.get_price() * p.get_quantity(),
                "description": p.get_description()
            })
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return filepath

    def export_inventory_report(self, warehouse: IWarehouse) -> str:
        filename = self._generate_filename("inventory", "txt")
        filepath = self._get_filepath(filename)
        
        inventory = warehouse.inventory_check()
        
        lines = []
        lines.append("=" * 60)
        lines.append("ЗВІТ ІНВЕНТАРИЗАЦІЇ СКЛАДУ")
        lines.append("=" * 60)
        lines.append(f"Дата: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
        lines.append(f"Склад: {inventory['назва_складу']}")
        lines.append(f"Локація: {inventory['локація']}")
        lines.append("-" * 60)
        lines.append(f"Загальна кількість товарів: {inventory['загальна_кількість_товарів']}")
        lines.append(f"Загальна кількість одиниць: {inventory['загальна_кількість_одиниць']}")
        lines.append(f"Загальна вартість: {inventory['загальна_вартість']:.2f} грн.")
        lines.append("-" * 60)
        lines.append("ТОВАРИ ЗА КАТЕГОРІЯМИ:")
        lines.append("")
        
        for category, data in inventory['категорії'].items():
            lines.append(f"  {category}:")
            lines.append(f"    Кількість товарів: {data['кількість_товарів']}")
            lines.append(f"    Кількість одиниць: {data['кількість_одиниць']}")
            lines.append(f"    Вартість: {data['вартість']:.2f} грн.")
            lines.append("")
        
        lines.append("=" * 60)
        lines.append("ДЕТАЛЬНИЙ СПИСОК ТОВАРІВ:")
        lines.append("-" * 60)
        
        for p in warehouse.get_all_products():
            lines.append(f"SKU: {p.get_sku()}")
            lines.append(f"  Назва: {p.get_name()}")
            lines.append(f"  Категорія: {p.get_category()}")
            lines.append(f"  Кількість: {p.get_quantity()}")
            lines.append(f"  Ціна: {p.get_price():.2f} грн.")
            lines.append(f"  Загальна вартість: {p.get_price() * p.get_quantity():.2f} грн.")
            lines.append("-" * 30)
        
        lines.append("=" * 60)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return filepath

    def list_exports(self) -> List[str]:
        if not os.path.exists(self._export_dir):
            return []
        return sorted(os.listdir(self._export_dir), reverse=True)

    def get_export_path(self, filename: str) -> str:
        return self._get_filepath(filename)

    def delete_export(self, filename: str) -> bool:
        filepath = self._get_filepath(filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False
