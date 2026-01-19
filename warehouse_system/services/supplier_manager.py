from typing import List, Dict, Optional
from interfaces.supplier_interface import ISupplier


class SupplierManager:
    def __init__(self):
        self._suppliers: Dict[str, ISupplier] = {}

    def add_supplier(self, supplier: ISupplier) -> bool:
        supplier_id = supplier.get_supplier_id()
        if supplier_id in self._suppliers:
            return False
        self._suppliers[supplier_id] = supplier
        return True

    def remove_supplier(self, supplier_id: str) -> bool:
        if supplier_id in self._suppliers:
            del self._suppliers[supplier_id]
            return True
        return False

    def get_supplier(self, supplier_id: str) -> Optional[ISupplier]:
        return self._suppliers.get(supplier_id)

    def get_all_suppliers(self) -> List[ISupplier]:
        return list(self._suppliers.values())

    def search_suppliers(self, keyword: str) -> List[ISupplier]:
        keyword_lower = keyword.lower()
        results = []
        for supplier in self._suppliers.values():
            if keyword_lower in supplier.get_name().lower():
                results.append(supplier)
                continue
            contact = supplier.get_contact_info()
            if keyword_lower in contact.get('адреса', '').lower():
                results.append(supplier)
        return results

    def get_suppliers_by_product(self, sku: str) -> List[ISupplier]:
        return [s for s in self._suppliers.values() 
                if sku in s.get_products_supplied()]

    def get_supplier_count(self) -> int:
        return len(self._suppliers)

    def get_statistics(self) -> Dict:
        total = len(self._suppliers)
        total_products = sum(len(s.get_products_supplied()) for s in self._suppliers.values())
        
        return {
            "загальна_кількість": total,
            "загальна_кількість_товарів": total_products,
            "середня_кількість_товарів": total_products / total if total > 0 else 0
        }

    def find_alternative_suppliers(self, sku: str, exclude_id: str = None) -> List[ISupplier]:
        suppliers = self.get_suppliers_by_product(sku)
        if exclude_id:
            suppliers = [s for s in suppliers if s.get_supplier_id() != exclude_id]
        return suppliers

    def export_contacts(self) -> List[Dict]:
        contacts = []
        for supplier in self._suppliers.values():
            contact_info = supplier.get_contact_info()
            contacts.append({
                "id": supplier.get_supplier_id(),
                "name": supplier.get_name(),
                "email": contact_info.get('електронна_пошта', ''),
                "phone": contact_info.get('телефон', ''),
                "address": contact_info.get('адреса', ''),
                "products_count": len(supplier.get_products_supplied())
            })
        return contacts
