import sys
sys.path.insert(0, '.')

from datetime import date, timedelta
from models.food_product import FoodProduct
from models.electronics_product import ElectronicsProduct
from models.clothing_product import ClothingProduct
from models.household_product import HouseholdProduct
from services.warehouse_service import Warehouse
from services.supplier_service import Supplier
from services.order_service import Order, OrderStatus
from services.report_service import InventoryReport, LowStockReport, SalesReport


def main():
    print("=" * 60)
    print("СИСТЕМА УПРАВЛІННЯ СКЛАДОМ")
    print("=" * 60)
    print()

    warehouse = Warehouse("Головний склад", "м. Київ, вул. Складська, 15")
    print(f"Створено склад: {warehouse.get_name()}")
    print(f"Локація: {warehouse.get_location()}")
    print()

    print("-" * 60)
    print("ДОДАВАННЯ ТОВАРІВ НА СКЛАД")
    print("-" * 60)

    food1 = FoodProduct(
        sku="FOOD-001",
        name="Молоко органічне 2.5%",
        price=45.50,
        quantity=100,
        description="Органічне молоко від українських фермерів",
        expiration_date=date.today() + timedelta(days=7),
        weight=1.0,
        is_organic=True
    )

    food2 = FoodProduct(
        sku="FOOD-002",
        name="Хліб пшеничний",
        price=25.00,
        quantity=50,
        description="Свіжий пшеничний хліб",
        expiration_date=date.today() + timedelta(days=3),
        weight=0.5,
        is_organic=False
    )

    electronics1 = ElectronicsProduct(
        sku="ELEC-001",
        name="Смартфон Galaxy A54",
        price=15999.00,
        quantity=25,
        description="Смартфон Samsung Galaxy A54 128GB",
        brand="Samsung",
        warranty_months=24,
        power_consumption=15.0
    )

    electronics2 = ElectronicsProduct(
        sku="ELEC-002",
        name="Ноутбук ThinkPad",
        price=32500.00,
        quantity=8,
        description="Бізнес-ноутбук Lenovo ThinkPad",
        brand="Lenovo",
        warranty_months=36,
        power_consumption=65.0
    )

    clothing1 = ClothingProduct(
        sku="CLOTH-001",
        name="Футболка базова",
        price=399.00,
        quantity=200,
        description="Бавовняна футболка унісекс",
        size="M",
        color="Чорний",
        material="100% бавовна",
        gender="Унісекс"
    )

    clothing2 = ClothingProduct(
        sku="CLOTH-002",
        name="Джинси класичні",
        price=1299.00,
        quantity=5,
        description="Класичні джинси прямого крою",
        size="32",
        color="Синій",
        material="Денім",
        gender="Чоловічий"
    )

    household1 = HouseholdProduct(
        sku="HOUSE-001",
        name="Стілець офісний",
        price=2850.00,
        quantity=15,
        description="Ергономічний офісний стілець",
        room_type="Офіс",
        dimensions={"width": 60, "height": 120, "depth": 60},
        weight=12.5
    )

    warehouse.add_product(food1)
    warehouse.add_product(food2)
    warehouse.add_product(electronics1)
    warehouse.add_product(electronics2)
    warehouse.add_product(clothing1)
    warehouse.add_product(clothing2)
    warehouse.add_product(household1)

    print(f"Додано товар: {food1}")
    print(f"Додано товар: {food2}")
    print(f"Додано товар: {electronics1}")
    print(f"Додано товар: {electronics2}")
    print(f"Додано товар: {clothing1}")
    print(f"Додано товар: {clothing2}")
    print(f"Додано товар: {household1}")
    print()

    print("-" * 60)
    print("ПОСТАЧАЛЬНИКИ")
    print("-" * 60)

    supplier1 = Supplier(
        supplier_id="SUP-001",
        name="ТОВ Електроніка Плюс",
        email="info@electronicsplus.ua",
        phone="+380441234567",
        address="м. Київ, вул. Технічна, 10"
    )
    supplier1.add_product_to_catalog("ELEC-001")
    supplier1.add_product_to_catalog("ELEC-002")

    supplier2 = Supplier(
        supplier_id="SUP-002",
        name="ФГ Українські Продукти",
        email="contact@ukrproducts.ua",
        phone="+380501112233",
        address="с. Веселе, Київська обл."
    )
    supplier2.add_product_to_catalog("FOOD-001")
    supplier2.add_product_to_catalog("FOOD-002")

    print(supplier1)
    print(f"  Контактна інформація: {supplier1.get_contact_info()}")
    print(f"  Товари: {supplier1.get_products_supplied()}")
    print()
    print(supplier2)
    print(f"  Контактна інформація: {supplier2.get_contact_info()}")
    print(f"  Товари: {supplier2.get_products_supplied()}")
    print()

    print("-" * 60)
    print("СТВОРЕННЯ ЗАМОВЛЕНЬ")
    print("-" * 60)

    order1 = Order()
    order1.add_item("ELEC-001", 2)
    order1.add_item("CLOTH-001", 5)
    order1.calculate_total(warehouse)
    print(order1)
    print(f"  Товари: {order1.get_items()}")
    print()

    order2 = Order()
    order2.add_item("FOOD-001", 10)
    order2.add_item("HOUSE-001", 1)
    order2.calculate_total(warehouse)
    print(order2)
    print(f"  Товари: {order2.get_items()}")
    print()

    print("-" * 60)
    print("ОБРОБКА ЗАМОВЛЕННЯ #1")
    print("-" * 60)

    if order1.process_order(warehouse):
        print("Замовлення успішно оброблено!")
        order1.set_status(OrderStatus.SHIPPED)
        print(f"Новий статус: {order1.get_status()}")
    else:
        print("Помилка обробки замовлення!")
    print()

    print("-" * 60)
    print("ПОШУК ТОВАРІВ")
    print("-" * 60)

    search_results = warehouse.search_products("смартфон")
    print(f"Результати пошуку за словом 'смартфон': {len(search_results)} товарів")
    for product in search_results:
        print(f"  - {product}")
    print()

    print("-" * 60)
    print("ТОВАРИ ЗА КАТЕГОРІЄЮ")
    print("-" * 60)

    electronics = warehouse.get_products_by_category("Електроніка")
    print(f"Категорія 'Електроніка': {len(electronics)} товарів")
    for product in electronics:
        print(f"  - {product}")
    print()

    print()
    inventory_report = InventoryReport(warehouse)
    print(inventory_report.generate())
    print()

    low_stock_report = LowStockReport(warehouse, threshold=10)
    print(low_stock_report.generate())
    print()

    orders = [order1, order2]
    sales_report = SalesReport(orders, warehouse)
    print(sales_report.generate())


if __name__ == "__main__":
    main()
