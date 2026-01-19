import os
import json
import shutil
from datetime import datetime
from typing import Dict, List, Optional


class BackupService:
    def __init__(self, backup_dir: str = "backups"):
        self._backup_dir = backup_dir
        self._ensure_backup_dir()

    def _ensure_backup_dir(self):
        if not os.path.exists(self._backup_dir):
            os.makedirs(self._backup_dir)

    def _get_filepath(self, filename: str) -> str:
        return os.path.join(self._backup_dir, filename)

    def _generate_backup_name(self) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"backup_{timestamp}.json"

    def create_backup(self, warehouse, suppliers: list, orders: list) -> str:
        backup_data = {
            "created_at": datetime.now().isoformat(),
            "version": "2.5",
            "warehouse": {
                "name": warehouse.get_name(),
                "location": warehouse.get_location(),
                "products": []
            },
            "suppliers": [],
            "orders": []
        }
        
        for product in warehouse.get_all_products():
            product_data = {
                "sku": product.get_sku(),
                "name": product.get_name(),
                "price": product.get_price(),
                "quantity": product.get_quantity(),
                "category": product.get_category(),
                "description": product.get_description()
            }
            
            if hasattr(product, 'get_expiration_date'):
                product_data["expiration_date"] = str(product.get_expiration_date())
                product_data["weight"] = product.get_weight()
                product_data["is_organic"] = product.is_organic()
                product_data["type"] = "food"
            
            elif hasattr(product, 'get_brand'):
                product_data["brand"] = product.get_brand()
                product_data["warranty_months"] = product.get_warranty_months()
                product_data["power_consumption"] = product.get_power_consumption()
                product_data["type"] = "electronics"
            
            elif hasattr(product, 'get_size'):
                product_data["size"] = product.get_size()
                product_data["color"] = product.get_color()
                product_data["material"] = product.get_material()
                product_data["gender"] = product.get_gender()
                product_data["type"] = "clothing"
            
            elif hasattr(product, 'get_room_type'):
                product_data["room_type"] = product.get_room_type()
                product_data["dimensions"] = product.get_dimensions()
                product_data["weight"] = product.get_weight()
                product_data["type"] = "household"
            
            backup_data["warehouse"]["products"].append(product_data)
        
        for supplier in suppliers:
            supplier_data = {
                "id": supplier.get_supplier_id(),
                "name": supplier.get_name(),
                "contact": supplier.get_contact_info(),
                "products": supplier.get_products_supplied()
            }
            backup_data["suppliers"].append(supplier_data)
        
        for order in orders:
            order_data = {
                "id": order.get_order_id(),
                "items": order.get_items(),
                "status": order.get_status(),
                "total": order.get_total_amount(),
                "created": order.get_created_date().isoformat()
            }
            backup_data["orders"].append(order_data)
        
        filename = self._generate_backup_name()
        filepath = self._get_filepath(filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(backup_data, f, ensure_ascii=False, indent=2, default=str)
        
        return filepath

    def list_backups(self) -> List[Dict]:
        backups = []
        if not os.path.exists(self._backup_dir):
            return backups
        
        for filename in sorted(os.listdir(self._backup_dir), reverse=True):
            if filename.endswith('.json'):
                filepath = self._get_filepath(filename)
                stat = os.stat(filepath)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        created_at = data.get('created_at', 'Невідомо')
                        products_count = len(data.get('warehouse', {}).get('products', []))
                except:
                    created_at = 'Невідомо'
                    products_count = 0
                
                backups.append({
                    "filename": filename,
                    "size": stat.st_size,
                    "created_at": created_at,
                    "products_count": products_count
                })
        
        return backups

    def load_backup(self, filename: str) -> Optional[Dict]:
        filepath = self._get_filepath(filename)
        if not os.path.exists(filepath):
            return None
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return None

    def delete_backup(self, filename: str) -> bool:
        filepath = self._get_filepath(filename)
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def get_backup_info(self, filename: str) -> Optional[Dict]:
        data = self.load_backup(filename)
        if not data:
            return None
        
        return {
            "filename": filename,
            "created_at": data.get('created_at'),
            "version": data.get('version'),
            "products_count": len(data.get('warehouse', {}).get('products', [])),
            "suppliers_count": len(data.get('suppliers', [])),
            "orders_count": len(data.get('orders', []))
        }

    def cleanup_old_backups(self, keep_count: int = 10) -> int:
        backups = self.list_backups()
        deleted = 0
        
        if len(backups) > keep_count:
            for backup in backups[keep_count:]:
                if self.delete_backup(backup['filename']):
                    deleted += 1
        
        return deleted
