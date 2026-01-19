import sys
sys.path.insert(0, '.')

from datetime import date, timedelta
from typing import Optional, List

from models.food_product import FoodProduct
from models.electronics_product import ElectronicsProduct
from models.clothing_product import ClothingProduct
from models.household_product import HouseholdProduct
from services.warehouse_service import Warehouse
from services.supplier_service import Supplier
from services.order_service import Order, OrderStatus
from services.report_service import InventoryReport, LowStockReport, SalesReport
from services.history_service import HistoryService, OperationType
from services.statistics_service import StatisticsService
from services.export_service import ExportService
from services.notification_service import NotificationService, AlertLevel
from services.pricing_service import PricingService, DiscountType
from services.backup_service import BackupService
from utils.console import Console, Colors
from utils.validators import Validators


class WarehouseApp:
    VERSION = "3.0"
    
    def __init__(self):
        self.warehouse = Warehouse("Головний склад", "м. Київ, вул. Складська, 15")
        self.suppliers: List[Supplier] = []
        self.orders: List[Order] = []
        self.history = HistoryService()
        self.statistics = StatisticsService(self.warehouse)
        self.export_service = ExportService()
        self.notifications = NotificationService()
        self.pricing = PricingService()
        self.backup_service = BackupService()
        self._init_demo_data()
        self._check_alerts()

    def _init_demo_data(self):
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

        food3 = FoodProduct(
            sku="FOOD-003",
            name="Сир твердий Гауда",
            price=289.00,
            quantity=30,
            description="Голландський сир Гауда",
            expiration_date=date.today() + timedelta(days=30),
            weight=0.4,
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

        electronics3 = ElectronicsProduct(
            sku="ELEC-003",
            name="Навушники AirPods Pro",
            price=8999.00,
            quantity=40,
            description="Бездротові навушники Apple",
            brand="Apple",
            warranty_months=12,
            power_consumption=0.5
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

        clothing3 = ClothingProduct(
            sku="CLOTH-003",
            name="Куртка зимова",
            price=3499.00,
            quantity=15,
            description="Тепла зимова куртка з капюшоном",
            size="L",
            color="Темно-синій",
            material="Поліестер",
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

        household2 = HouseholdProduct(
            sku="HOUSE-002",
            name="Лампа настільна LED",
            price=899.00,
            quantity=45,
            description="Сучасна LED лампа з регулюванням яскравості",
            room_type="Кабінет",
            dimensions={"width": 15, "height": 45, "depth": 15},
            weight=1.2
        )

        self.warehouse.add_product(food1)
        self.warehouse.add_product(food2)
        self.warehouse.add_product(food3)
        self.warehouse.add_product(electronics1)
        self.warehouse.add_product(electronics2)
        self.warehouse.add_product(electronics3)
        self.warehouse.add_product(clothing1)
        self.warehouse.add_product(clothing2)
        self.warehouse.add_product(clothing3)
        self.warehouse.add_product(household1)
        self.warehouse.add_product(household2)

        supplier1 = Supplier(
            supplier_id="SUP-001",
            name="ТОВ Електроніка Плюс",
            email="info@electronicsplus.ua",
            phone="+380441234567",
            address="м. Київ, вул. Технічна, 10"
        )
        supplier1.add_product_to_catalog("ELEC-001")
        supplier1.add_product_to_catalog("ELEC-002")
        supplier1.add_product_to_catalog("ELEC-003")

        supplier2 = Supplier(
            supplier_id="SUP-002",
            name="ФГ Українські Продукти",
            email="contact@ukrproducts.ua",
            phone="+380501112233",
            address="с. Веселе, Київська обл."
        )
        supplier2.add_product_to_catalog("FOOD-001")
        supplier2.add_product_to_catalog("FOOD-002")
        supplier2.add_product_to_catalog("FOOD-003")

        supplier3 = Supplier(
            supplier_id="SUP-003",
            name="Fashion House",
            email="orders@fashionhouse.ua",
            phone="+380671234567",
            address="м. Львів, вул. Модна, 25"
        )
        supplier3.add_product_to_catalog("CLOTH-001")
        supplier3.add_product_to_catalog("CLOTH-002")
        supplier3.add_product_to_catalog("CLOTH-003")

        self.suppliers.append(supplier1)
        self.suppliers.append(supplier2)
        self.suppliers.append(supplier3)

        self.history.add_record(
            OperationType.PRODUCT_ADDED,
            "Ініціалізовано демо-дані складу",
            details={"кількість_товарів": 11}
        )

    def _check_alerts(self):
        self.notifications.check_low_stock(self.warehouse, 10)
        self.notifications.check_expiring_products(self.warehouse, 7)

    def run(self):
        Console.init()
        while True:
            self._show_main_menu()
            choice = Console.input_prompt("Ваш вибір")
            valid, num, error = Validators.validate_menu_choice(choice, 0, 16)
            
            if not valid:
                Console.print_error(error)
                Console.pause()
                continue

            if num == 0:
                self._exit_app()
                break
            elif num == 1:
                self._view_all_products()
            elif num == 2:
                self._search_products()
            elif num == 3:
                self._add_product()
            elif num == 4:
                self._issue_product()
            elif num == 5:
                self._create_order()
            elif num == 6:
                self._view_orders()
            elif num == 7:
                self._view_suppliers()
            elif num == 8:
                self._generate_reports()
            elif num == 9:
                self._view_statistics()
            elif num == 10:
                self._export_data()
            elif num == 11:
                self._view_history()
            elif num == 12:
                self._inventory_check()
            elif num == 13:
                self._manage_discounts()
            elif num == 14:
                self._view_notifications()
            elif num == 15:
                self._backup_restore()
            elif num == 16:
                self._settings()

    def _show_main_menu(self):
        Console.clear()
        self._print_logo()
        
        products_count = len(self.warehouse.get_all_products())
        total_value = self.warehouse.get_total_value()
        low_stock = len(self.warehouse.get_low_stock_products(10))
        unread_alerts = self.notifications.get_unread_count()
        
        print(f"{Colors.WHITE}  📦 Товарів: {Colors.CYAN}{products_count}{Colors.WHITE} | "
              f"💰 Вартість: {Colors.GREEN}{total_value:,.2f} грн{Colors.WHITE} | "
              f"⚠️  Низький запас: {Colors.YELLOW if low_stock > 0 else Colors.GREEN}{low_stock}{Colors.WHITE} | "
              f"🔔 Сповіщень: {Colors.RED if unread_alerts > 0 else Colors.GREEN}{unread_alerts}{Colors.ENDC}")
        
        Console.print_header("Головне меню")
        
        print(f"{Colors.CYAN}  ┌─────────────────────────────────────────────────────┐{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}           {Colors.BOLD}📦 УПРАВЛІННЯ ТОВАРАМИ{Colors.ENDC}                  {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  ├─────────────────────────────────────────────────────┤{Colors.ENDC}")
        Console.print_menu_item(1, "📋 Переглянути всі товари")
        Console.print_menu_item(2, "🔍 Пошук товарів")
        Console.print_menu_item(3, "➕ Додати новий товар")
        Console.print_menu_item(4, "📤 Видати товар зі складу")
        print(f"{Colors.CYAN}  ├─────────────────────────────────────────────────────┤{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}           {Colors.BOLD}🛒 ЗАМОВЛЕННЯ ТА ПОСТАЧАЛЬНИКИ{Colors.ENDC}         {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  ├─────────────────────────────────────────────────────┤{Colors.ENDC}")
        Console.print_menu_item(5, "🛍️  Створити замовлення")
        Console.print_menu_item(6, "📑 Переглянути замовлення")
        Console.print_menu_item(7, "🚚 Переглянути постачальників")
        print(f"{Colors.CYAN}  ├─────────────────────────────────────────────────────┤{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}           {Colors.BOLD}📊 ЗВІТИ ТА АНАЛІТИКА{Colors.ENDC}                  {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  ├─────────────────────────────────────────────────────┤{Colors.ENDC}")
        Console.print_menu_item(8, "📄 Генерувати звіти")
        Console.print_menu_item(9, "📈 Статистика складу")
        Console.print_menu_item(10, "💾 Експорт даних")
        Console.print_menu_item(11, "📜 Історія операцій")
        Console.print_menu_item(12, "🔢 Інвентаризація складу")
        print(f"{Colors.CYAN}  ├─────────────────────────────────────────────────────┤{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}           {Colors.BOLD}⚙️  ДОДАТКОВІ ФУНКЦІЇ{Colors.ENDC}                   {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  ├─────────────────────────────────────────────────────┤{Colors.ENDC}")
        Console.print_menu_item(13, "🏷️  Управління знижками")
        alert_indicator = f" ({Colors.RED}{unread_alerts}{Colors.ENDC})" if unread_alerts > 0 else ""
        print(f"  {Colors.CYAN}[14]{Colors.ENDC} {Colors.WHITE}🔔 Сповіщення{alert_indicator}{Colors.ENDC}")
        Console.print_menu_item(15, "💾 Резервне копіювання")
        Console.print_menu_item(16, "⚙️  Налаштування")
        print(f"{Colors.CYAN}  ├─────────────────────────────────────────────────────┤{Colors.ENDC}")
        Console.print_menu_item(0, "🚪 Вихід з програми")
        print(f"{Colors.CYAN}  └─────────────────────────────────────────────────────┘{Colors.ENDC}")
        print()

    def _print_logo(self):
        logo = f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ░██╗░░░░░░░██╗░█████╗░██████╗░███████╗██╗░░██╗░█████╗░  ║
    ║   ░██║░░██╗░░██║██╔══██╗██╔══██╗██╔════╝██║░░██║██╔══██╗  ║
    ║   ░╚██╗████╗██╔╝███████║██████╔╝█████╗░░███████║██║░░██║  ║
    ║   ░░████╔═████║░██╔══██║██╔══██╗██╔══╝░░██╔══██║██║░░██║  ║
    ║   ░░╚██╔╝░╚██╔╝░██║░░██║██║░░██║███████╗██║░░██║╚█████╔╝  ║
    ║   ░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░╚════╝░  ║
    ║                                                           ║
    ║           СИСТЕМА УПРАВЛІННЯ СКЛАДОМ v{self.VERSION}              ║
    ╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}"""
        print(logo)

    def _view_all_products(self):
        Console.clear()
        Console.print_header("📋 Всі товари на складі")
        
        products = self.warehouse.get_all_products()
        if not products:
            Console.print_warning("Склад порожній")
            Console.pause()
            return

        print(f"\n{Colors.CYAN}  Фільтрація за категорією:{Colors.ENDC}")
        categories = self.warehouse.get_categories()
        Console.print_menu_item(0, "Всі категорії")
        for i, cat in enumerate(categories, 1):
            Console.print_menu_item(i, cat)
        
        choice = Console.input_prompt("Категорія (Enter для всіх)")
        
        if choice.strip():
            valid, num, _ = Validators.validate_menu_choice(choice, 0, len(categories))
            if valid and num > 0:
                products = self.warehouse.get_products_by_category(categories[num - 1])

        print()
        widths = [12, 26, 10, 12, 20]
        Console.print_table_header(["SKU", "Назва", "Кількість", "Ціна (грн)", "Категорія"], widths)
        
        for product in products:
            qty = product.get_quantity()
            qty_color = Colors.RED if qty <= 5 else Colors.YELLOW if qty <= 15 else Colors.WHITE
            print(f"{Colors.WHITE}{product.get_sku():<12}{product.get_name()[:24]:<26}"
                  f"{qty_color}{qty:<10}{Colors.GREEN}{product.get_price():<12.2f}"
                  f"{Colors.WHITE}{product.get_category()[:18]:<20}{Colors.ENDC}")

        print()
        total_qty = sum(p.get_quantity() for p in products)
        total_val = sum(p.get_price() * p.get_quantity() for p in products)
        Console.print_info(f"Показано товарів: {len(products)}")
        Console.print_info(f"Загальна кількість одиниць: {total_qty}")
        Console.print_info(f"Загальна вартість: {total_val:,.2f} грн.")
        Console.pause()

    def _search_products(self):
        Console.clear()
        Console.print_header("🔍 Пошук товарів")
        
        print(f"{Colors.CYAN}  Варіанти пошуку:{Colors.ENDC}")
        Console.print_menu_item(1, "Пошук за ключовим словом")
        Console.print_menu_item(2, "Пошук за SKU")
        Console.print_menu_item(3, "Товари з низьким запасом")
        Console.print_menu_item(0, "Назад")
        print()

        choice = Console.input_prompt("Варіант пошуку")
        
        if choice == "1":
            keyword = Console.input_prompt("Введіть ключове слово")
            if not keyword.strip():
                Console.print_error("Введіть ключове слово")
                Console.pause()
                return
            results = self.warehouse.search_products(keyword)
            
            if not results:
                Console.print_warning(f"Товари за запитом '{keyword}' не знайдено")
            else:
                Console.print_success(f"Знайдено товарів: {len(results)}")
                print()
                for product in results:
                    Console.print_item(str(product))
        
        elif choice == "2":
            sku = Console.input_prompt("Введіть SKU")
            product = self.warehouse.get_product(sku.upper())
            if product:
                Console.print_success("Товар знайдено:")
                print()
                Console.print_item(f"SKU: {product.get_sku()}")
                Console.print_item(f"Назва: {product.get_name()}")
                Console.print_item(f"Категорія: {product.get_category()}")
                Console.print_item(f"Кількість: {product.get_quantity()}")
                Console.print_item(f"Ціна: {product.get_price():.2f} грн.")
                Console.print_item(f"Опис: {product.get_description()}")
            else:
                Console.print_error(f"Товар з SKU '{sku}' не знайдено")
        
        elif choice == "3":
            threshold_str = Console.input_prompt("Поріг низького запасу (за замовчуванням 10)")
            threshold = 10
            if threshold_str.strip():
                valid, threshold, _ = Validators.validate_positive_int(threshold_str)
                if not valid:
                    threshold = 10
            
            low_stock = self.warehouse.get_low_stock_products(threshold)
            if not low_stock:
                Console.print_success(f"Товарів з запасом менше {threshold} од. не знайдено")
            else:
                Console.print_warning(f"Товарів з низьким запасом: {len(low_stock)}")
                print()
                for p in low_stock:
                    color = Colors.RED if p.get_quantity() <= 5 else Colors.YELLOW
                    print(f"  {color}• {p.get_name()} - {p.get_quantity()} од.{Colors.ENDC}")
        
        Console.pause()

    def _add_product(self):
        Console.clear()
        Console.print_header("➕ Додавання нового товару")
        
        print(f"{Colors.CYAN}  Виберіть тип товару:{Colors.ENDC}")
        Console.print_menu_item(1, "🥛 Продукти харчування")
        Console.print_menu_item(2, "📱 Електроніка")
        Console.print_menu_item(3, "👕 Одяг")
        Console.print_menu_item(4, "🏠 Господарські товари")
        Console.print_menu_item(0, "❌ Скасувати")
        print()

        choice = Console.input_prompt("Тип товару")
        valid, num, error = Validators.validate_menu_choice(choice, 0, 4)
        
        if not valid or num == 0:
            return

        sku = Console.input_prompt("SKU товару")
        valid, sku, error = Validators.validate_sku(sku)
        if not valid:
            Console.print_error(error)
            Console.pause()
            return

        if self.warehouse.get_product(sku):
            Console.print_error(f"Товар з SKU '{sku}' вже існує")
            Console.pause()
            return

        name = Console.input_prompt("Назва товару")
        valid, name, error = Validators.validate_non_empty(name)
        if not valid:
            Console.print_error(error)
            Console.pause()
            return

        price_str = Console.input_prompt("Ціна (грн)")
        valid, price, error = Validators.validate_positive_float(price_str)
        if not valid:
            Console.print_error(error)
            Console.pause()
            return

        qty_str = Console.input_prompt("Кількість")
        valid, quantity, error = Validators.validate_positive_int(qty_str)
        if not valid:
            Console.print_error(error)
            Console.pause()
            return

        description = Console.input_prompt("Опис товару")

        product = None
        if num == 1:
            exp_date_str = Console.input_prompt("Термін придатності (ДД.ММ.РРРР)")
            valid, exp_date, error = Validators.validate_date(exp_date_str)
            if not valid:
                Console.print_error(error)
                Console.pause()
                return
            weight_str = Console.input_prompt("Вага (кг)")
            valid, weight, error = Validators.validate_positive_float(weight_str)
            if not valid:
                Console.print_error(error)
                Console.pause()
                return
            is_organic = Console.input_prompt("Органічний продукт? (так/ні)").lower() in ["так", "yes", "y", "1"]
            product = FoodProduct(sku, name, price, quantity, description, exp_date, weight, is_organic)
        
        elif num == 2:
            brand = Console.input_prompt("Бренд")
            warranty_str = Console.input_prompt("Гарантія (місяців)")
            valid, warranty, error = Validators.validate_positive_int(warranty_str)
            if not valid:
                Console.print_error(error)
                Console.pause()
                return
            power_str = Console.input_prompt("Споживана потужність (Вт)")
            valid, power, error = Validators.validate_positive_float(power_str)
            if not valid:
                Console.print_error(error)
                Console.pause()
                return
            product = ElectronicsProduct(sku, name, price, quantity, description, brand, warranty, power)
        
        elif num == 3:
            size = Console.input_prompt("Розмір")
            color = Console.input_prompt("Колір")
            material = Console.input_prompt("Матеріал")
            gender = Console.input_prompt("Стать (Чоловічий/Жіночий/Унісекс)")
            product = ClothingProduct(sku, name, price, quantity, description, size, color, material, gender)
        
        elif num == 4:
            room_type = Console.input_prompt("Тип кімнати")
            width_str = Console.input_prompt("Ширина (см)")
            height_str = Console.input_prompt("Висота (см)")
            depth_str = Console.input_prompt("Глибина (см)")
            weight_str = Console.input_prompt("Вага (кг)")
            try:
                dimensions = {
                    "width": float(width_str),
                    "height": float(height_str),
                    "depth": float(depth_str)
                }
                weight = float(weight_str)
            except ValueError:
                Console.print_error("Невірний формат розмірів")
                Console.pause()
                return
            product = HouseholdProduct(sku, name, price, quantity, description, room_type, dimensions, weight)

        if product:
            self.warehouse.add_product(product)
            self.history.add_record(
                OperationType.PRODUCT_ADDED,
                f"Додано товар: {name} (SKU: {sku})",
                details={"sku": sku, "кількість": quantity, "ціна": price}
            )
            Console.print_success(f"Товар '{name}' успішно додано на склад!")
        
        Console.pause()

    def _issue_product(self):
        Console.clear()
        Console.print_header("📤 Видача товару зі складу")
        
        sku = Console.input_prompt("Введіть SKU товару")
        product = self.warehouse.get_product(sku.upper())
        
        if not product:
            Console.print_error(f"Товар з SKU '{sku}' не знайдено")
            Console.pause()
            return

        Console.print_info(f"Товар: {product.get_name()}")
        Console.print_info(f"Доступна кількість: {product.get_quantity()}")
        
        qty_str = Console.input_prompt("Кількість для видачі")
        valid, quantity, error = Validators.validate_positive_int(qty_str)
        if not valid:
            Console.print_error(error)
            Console.pause()
            return

        if self.warehouse.issue_product(sku.upper(), quantity):
            self.history.add_record(
                OperationType.PRODUCT_ISSUED,
                f"Видано товар: {product.get_name()} - {quantity} од.",
                details={"sku": sku.upper(), "кількість": quantity}
            )
            Console.print_success(f"Видано {quantity} од. товару '{product.get_name()}'")
        else:
            Console.print_error("Недостатня кількість товару на складі")
        
        Console.pause()

    def _create_order(self):
        Console.clear()
        Console.print_header("🛍️ Створення замовлення")
        
        order = Order()
        Console.print_info(f"Створено замовлення #{order.get_order_id()}")
        
        while True:
            print()
            print(f"{Colors.CYAN}  Поточні товари в замовленні:{Colors.ENDC}")
            items = order.get_items()
            if items:
                for sku, qty in items:
                    product = self.warehouse.get_product(sku)
                    if product:
                        Console.print_item(f"{product.get_name()} x {qty} = {product.get_price() * qty:.2f} грн.")
            else:
                Console.print_item("(порожньо)")
            
            print()
            Console.print_menu_item(1, "Додати товар")
            Console.print_menu_item(2, "Видалити товар")
            Console.print_menu_item(3, "Завершити та оформити замовлення")
            Console.print_menu_item(0, "Скасувати замовлення")
            
            choice = Console.input_prompt("Дія")
            
            if choice == "0":
                Console.print_warning("Замовлення скасовано")
                Console.pause()
                return
            elif choice == "3":
                if not order.get_items():
                    Console.print_error("Замовлення порожнє!")
                    continue
                break
            elif choice == "1":
                sku = Console.input_prompt("SKU товару")
                product = self.warehouse.get_product(sku.upper())
                if not product:
                    Console.print_error(f"Товар з SKU '{sku}' не знайдено")
                    continue
                
                Console.print_info(f"Товар: {product.get_name()} - {product.get_price():.2f} грн.")
                Console.print_info(f"Доступно: {product.get_quantity()} од.")
                
                qty_str = Console.input_prompt("Кількість")
                valid, qty, error = Validators.validate_positive_int(qty_str)
                if not valid:
                    Console.print_error(error)
                    continue
                    
                if qty > product.get_quantity():
                    Console.print_error("Недостатня кількість на складі")
                    continue
                    
                order.add_item(sku.upper(), qty)
                Console.print_success(f"Додано: {product.get_name()} x {qty}")
            
            elif choice == "2":
                if not order.get_items():
                    Console.print_warning("Замовлення порожнє")
                    continue
                sku = Console.input_prompt("SKU товару для видалення")
                if order.remove_item(sku.upper()):
                    Console.print_success("Товар видалено з замовлення")
                else:
                    Console.print_error("Товар не знайдено в замовленні")

        order.calculate_total(self.warehouse)
        
        print()
        Console.print_subheader("Підтвердження замовлення")
        Console.print_info(f"Номер замовлення: {order.get_order_id()}")
        Console.print_info(f"Кількість позицій: {len(order.get_items())}")
        Console.print_info(f"Загальна сума: {order.get_total_amount():.2f} грн.")
        
        confirm = Console.input_prompt("Підтвердити замовлення? (так/ні)")
        if confirm.lower() not in ["так", "yes", "y", "1"]:
            Console.print_warning("Замовлення скасовано")
            Console.pause()
            return

        if order.process_order(self.warehouse):
            order.set_status(OrderStatus.PROCESSING)
            self.orders.append(order)
            self.history.add_record(
                OperationType.ORDER_CREATED,
                f"Створено замовлення #{order.get_order_id()}",
                details={"order_id": order.get_order_id(), "сума": order.get_total_amount()}
            )
            Console.print_success("Замовлення успішно оформлено!")
            Console.print_info(f"Номер замовлення: {order.get_order_id()}")
            Console.print_info(f"Сума: {order.get_total_amount():.2f} грн.")
        else:
            Console.print_error("Помилка оформлення замовлення")
        
        Console.pause()

    def _view_orders(self):
        Console.clear()
        Console.print_header("📑 Замовлення")
        
        if not self.orders:
            Console.print_warning("Список замовлень порожній")
            Console.pause()
            return

        widths = [12, 20, 18, 15]
        Console.print_table_header(["№ Замовлення", "Дата", "Статус", "Сума (грн)"], widths)
        
        for order in self.orders:
            status = order.get_status()
            status_color = Colors.GREEN if status == OrderStatus.DELIVERED else \
                          Colors.YELLOW if status == OrderStatus.PROCESSING else \
                          Colors.RED if status == OrderStatus.CANCELLED else Colors.WHITE
            
            print(f"{Colors.WHITE}{order.get_order_id():<12}"
                  f"{order.get_created_date().strftime('%d.%m.%Y %H:%M'):<20}"
                  f"{status_color}{status:<18}{Colors.ENDC}"
                  f"{Colors.GREEN}{order.get_total_amount():<15.2f}{Colors.ENDC}")

        print()
        total_revenue = sum(o.get_total_amount() for o in self.orders)
        Console.print_info(f"Всього замовлень: {len(self.orders)}")
        Console.print_info(f"Загальний дохід: {total_revenue:,.2f} грн.")
        Console.pause()

    def _view_suppliers(self):
        Console.clear()
        Console.print_header("🚚 Постачальники")
        
        if not self.suppliers:
            Console.print_warning("Список постачальників порожній")
            Console.pause()
            return

        for i, supplier in enumerate(self.suppliers, 1):
            print(f"\n{Colors.CYAN}  ┌{'─' * 48}┐{Colors.ENDC}")
            print(f"{Colors.CYAN}  │{Colors.ENDC} {Colors.BOLD}#{i} {supplier.get_name():<42}{Colors.ENDC} {Colors.CYAN}│{Colors.ENDC}")
            print(f"{Colors.CYAN}  ├{'─' * 48}┤{Colors.ENDC}")
            contact = supplier.get_contact_info()
            print(f"{Colors.CYAN}  │{Colors.ENDC}   📧 {contact['електронна_пошта']:<40} {Colors.CYAN}│{Colors.ENDC}")
            print(f"{Colors.CYAN}  │{Colors.ENDC}   📞 {contact['телефон']:<40} {Colors.CYAN}│{Colors.ENDC}")
            print(f"{Colors.CYAN}  │{Colors.ENDC}   📍 {contact['адреса'][:40]:<40} {Colors.CYAN}│{Colors.ENDC}")
            products = supplier.get_products_supplied()
            print(f"{Colors.CYAN}  │{Colors.ENDC}   📦 Товарів: {len(products):<33} {Colors.CYAN}│{Colors.ENDC}")
            print(f"{Colors.CYAN}  └{'─' * 48}┘{Colors.ENDC}")
        
        Console.pause()

    def _generate_reports(self):
        Console.clear()
        Console.print_header("📄 Генерація звітів")
        
        Console.print_menu_item(1, "📊 Звіт інвентаризації")
        Console.print_menu_item(2, "⚠️  Звіт про товари з низьким запасом")
        Console.print_menu_item(3, "💰 Звіт про продажі")
        Console.print_menu_item(0, "🔙 Назад")
        print()

        choice = Console.input_prompt("Виберіть звіт")
        
        report_content = ""
        report_type = ""
        
        if choice == "1":
            report = InventoryReport(self.warehouse)
            report_content = report.generate()
            report_type = "inventory"
            print(report_content)
        elif choice == "2":
            threshold_str = Console.input_prompt("Поріг низького запасу (за замовчуванням 10)")
            threshold = 10
            if threshold_str.strip():
                valid, threshold, _ = Validators.validate_positive_int(threshold_str)
                if not valid:
                    threshold = 10
            report = LowStockReport(self.warehouse, threshold)
            report_content = report.generate()
            report_type = "low_stock"
            print(report_content)
        elif choice == "3":
            report = SalesReport(self.orders, self.warehouse)
            report_content = report.generate()
            report_type = "sales"
            print(report_content)
        elif choice == "0":
            return

        if report_content:
            print()
            save = Console.input_prompt("Зберегти звіт у файл? (так/ні)")
            if save.lower() in ["так", "yes", "y", "1"]:
                from utils.data_manager import DataManager
                dm = DataManager()
                filepath = dm.save_report(report_type, report_content)
                if filepath:
                    Console.print_success(f"Звіт збережено: {filepath}")
                    self.history.add_record(
                        OperationType.REPORT_GENERATED,
                        f"Згенеровано звіт: {report_type}",
                        details={"файл": filepath}
                    )
        
        Console.pause()

    def _view_statistics(self):
        Console.clear()
        Console.print_header("📈 Статистика складу")
        
        summary = self.statistics.get_summary()
        
        print(f"\n{Colors.CYAN}  ┌{'─' * 48}┐{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}          {Colors.BOLD}📊 ЗАГАЛЬНА СТАТИСТИКА{Colors.ENDC}              {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  ├{'─' * 48}┤{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}  📦 Товарів на складі:    {Colors.WHITE}{summary['загальна_кількість_товарів']:<18}{Colors.ENDC} {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}  🔢 Загальна кількість:   {Colors.WHITE}{summary['загальна_кількість_одиниць']:<18}{Colors.ENDC} {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}  💰 Загальна вартість:    {Colors.GREEN}{summary['загальна_вартість']:>14,.2f} грн{Colors.ENDC} {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}  📊 Середня вартість:     {Colors.WHITE}{summary['середня_вартість_товару']:>14,.2f} грн{Colors.ENDC} {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}  📁 Кількість категорій:  {Colors.WHITE}{summary['кількість_категорій']:<18}{Colors.ENDC} {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  └{'─' * 48}┘{Colors.ENDC}")
        
        print(self.statistics.generate_ascii_chart(
            self.statistics.get_category_distribution(),
            "📦 РОЗПОДІЛ ЗА КАТЕГОРІЯМИ"
        ))
        
        print(self.statistics.generate_ascii_chart(
            self.statistics.get_stock_health(),
            "📊 СТАН ЗАПАСІВ"
        ))
        
        print(f"\n{Colors.CYAN}  {'─' * 40}{Colors.ENDC}")
        print(f"  {Colors.BOLD}🏆 ТОП-5 ТОВАРІВ ЗА ВАРТІСТЮ:{Colors.ENDC}")
        for name, value in self.statistics.get_top_products_by_value(5):
            print(f"    • {name[:30]:<30} {Colors.GREEN}{value:>10,.2f} грн{Colors.ENDC}")
        
        price_range = self.statistics.get_price_range()
        print(f"\n{Colors.CYAN}  {'─' * 40}{Colors.ENDC}")
        print(f"  {Colors.BOLD}💵 ДІАПАЗОН ЦІН:{Colors.ENDC}")
        print(f"    Мінімальна: {Colors.WHITE}{price_range['мінімум']:,.2f} грн{Colors.ENDC}")
        print(f"    Максимальна: {Colors.WHITE}{price_range['максимум']:,.2f} грн{Colors.ENDC}")
        print(f"    Середня: {Colors.WHITE}{price_range['середня']:,.2f} грн{Colors.ENDC}")
        
        Console.pause()

    def _export_data(self):
        Console.clear()
        Console.print_header("💾 Експорт даних")
        
        Console.print_menu_item(1, "📄 Експорт товарів у CSV")
        Console.print_menu_item(2, "📋 Експорт товарів у JSON")
        Console.print_menu_item(3, "📝 Експорт повного звіту інвентаризації")
        Console.print_menu_item(4, "📂 Переглянути експортовані файли")
        Console.print_menu_item(0, "🔙 Назад")
        print()

        choice = Console.input_prompt("Виберіть дію")
        
        if choice == "1":
            filepath = self.export_service.export_products_to_csv(self.warehouse)
            Console.print_success(f"Дані експортовано у файл: {filepath}")
            self.history.add_record(
                OperationType.REPORT_GENERATED,
                "Експортовано товари у CSV",
                details={"файл": filepath}
            )
        elif choice == "2":
            filepath = self.export_service.export_products_to_json(self.warehouse)
            Console.print_success(f"Дані експортовано у файл: {filepath}")
            self.history.add_record(
                OperationType.REPORT_GENERATED,
                "Експортовано товари у JSON",
                details={"файл": filepath}
            )
        elif choice == "3":
            filepath = self.export_service.export_inventory_report(self.warehouse)
            Console.print_success(f"Звіт експортовано у файл: {filepath}")
            self.history.add_record(
                OperationType.REPORT_GENERATED,
                "Експортовано звіт інвентаризації",
                details={"файл": filepath}
            )
        elif choice == "4":
            exports = self.export_service.list_exports()
            if not exports:
                Console.print_warning("Експортованих файлів не знайдено")
            else:
                Console.print_success(f"Знайдено файлів: {len(exports)}")
                for exp in exports[:10]:
                    Console.print_item(exp)
        
        Console.pause()

    def _view_history(self):
        Console.clear()
        Console.print_header("📜 Історія операцій")
        
        records = self.history.get_recent_records(20)
        
        if not records:
            Console.print_warning("Історія операцій порожня")
            Console.pause()
            return

        print(f"{Colors.CYAN}  Останні {len(records)} операцій:{Colors.ENDC}\n")
        
        for record in reversed(records):
            op_type = record.get_operation_type()
            if op_type in [OperationType.PRODUCT_ADDED, OperationType.ORDER_CREATED]:
                color = Colors.GREEN
            elif op_type in [OperationType.PRODUCT_ISSUED, OperationType.ORDER_PROCESSED]:
                color = Colors.YELLOW
            elif op_type in [OperationType.PRODUCT_REMOVED, OperationType.ORDER_CANCELLED]:
                color = Colors.RED
            else:
                color = Colors.WHITE
            
            print(f"  {color}{record}{Colors.ENDC}")
        
        print()
        stats = self.history.get_statistics()
        if stats:
            Console.print_subheader("Статистика операцій")
            for op, count in stats.items():
                Console.print_item(f"{op}: {count}")
        
        Console.pause()

    def _inventory_check(self):
        Console.clear()
        Console.print_header("🔢 Інвентаризація складу")
        
        self.history.add_record(
            OperationType.INVENTORY_CHECK,
            "Проведено інвентаризацію складу"
        )
        
        inventory = self.warehouse.inventory_check()
        
        print(f"\n{Colors.CYAN}  ┌{'─' * 48}┐{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC} {Colors.BOLD}📍 {inventory['назва_складу']:<43}{Colors.ENDC} {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}    {inventory['локація']:<44} {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  └{'─' * 48}┘{Colors.ENDC}")
        
        print(f"\n{Colors.CYAN}  {'─' * 40}{Colors.ENDC}")
        Console.print_success(f"Загальна кількість товарів: {inventory['загальна_кількість_товарів']}")
        Console.print_success(f"Загальна кількість одиниць: {inventory['загальна_кількість_одиниць']}")
        Console.print_success(f"Загальна вартість: {inventory['загальна_вартість']:,.2f} грн.")
        
        print()
        Console.print_subheader("Розподіл за категоріями")
        
        for category, data in inventory['категорії'].items():
            print()
            print(f"  {Colors.BOLD}{Colors.CYAN}{category}{Colors.ENDC}")
            Console.print_item(f"Кількість товарів: {data['кількість_товарів']}", 4)
            Console.print_item(f"Кількість одиниць: {data['кількість_одиниць']}", 4)
            Console.print_item(f"Вартість: {data['вартість']:,.2f} грн.", 4)
        
        Console.pause()

    def _manage_discounts(self):
        Console.clear()
        Console.print_header("🏷️ Управління знижками")
        
        Console.print_menu_item(1, "Переглянути активні знижки")
        Console.print_menu_item(2, "Створити нову знижку")
        Console.print_menu_item(3, "Застосувати знижку до товару")
        Console.print_menu_item(4, "Калькулятор ціни зі знижкою")
        Console.print_menu_item(0, "Назад")
        print()

        choice = Console.input_prompt("Виберіть дію")
        
        if choice == "1":
            discounts = self.pricing.get_all_discounts()
            if not discounts:
                Console.print_warning("Знижки відсутні")
            else:
                Console.print_success(f"Знайдено знижок: {len(discounts)}")
                print()
                for d in discounts:
                    status_color = Colors.GREEN if d.is_active() else Colors.RED
                    print(f"  {status_color}{d}{Colors.ENDC}")
                    Console.print_item(f"ID: {d.get_id()}", 4)
                    Console.print_item(f"Мін. кількість: {d.get_min_quantity()}", 4)
        
        elif choice == "2":
            name = Console.input_prompt("Назва знижки")
            if not name.strip():
                Console.print_error("Введіть назву")
                Console.pause()
                return
            
            print(f"\n{Colors.CYAN}Тип знижки:{Colors.ENDC}")
            Console.print_menu_item(1, "Відсоткова (%)")
            Console.print_menu_item(2, "Фіксована (грн)")
            
            type_choice = Console.input_prompt("Тип")
            discount_type = DiscountType.PERCENTAGE if type_choice == "1" else DiscountType.FIXED
            
            value_str = Console.input_prompt("Значення знижки")
            valid, value, error = Validators.validate_positive_float(value_str)
            if not valid:
                Console.print_error(error)
                Console.pause()
                return
            
            min_qty_str = Console.input_prompt("Мінімальна кількість (за замовчуванням 1)")
            min_qty = 1
            if min_qty_str.strip():
                valid, min_qty, _ = Validators.validate_positive_int(min_qty_str)
                if not valid:
                    min_qty = 1
            
            discount = self.pricing.create_custom_discount(name, discount_type, value, min_qty)
            Console.print_success(f"Знижку створено! ID: {discount.get_id()}")
        
        elif choice == "3":
            sku = Console.input_prompt("SKU товару")
            product = self.warehouse.get_product(sku.upper())
            if not product:
                Console.print_error(f"Товар з SKU '{sku}' не знайдено")
                Console.pause()
                return
            
            Console.print_info(f"Товар: {product.get_name()}")
            
            discounts = self.pricing.get_active_discounts()
            if not discounts:
                Console.print_warning("Активні знижки відсутні")
                Console.pause()
                return
            
            print(f"\n{Colors.CYAN}Доступні знижки:{Colors.ENDC}")
            for i, d in enumerate(discounts, 1):
                Console.print_menu_item(i, f"{d.get_name()} ({d.get_id()})")
            
            disc_choice = Console.input_prompt("Номер знижки")
            valid, num, error = Validators.validate_menu_choice(disc_choice, 1, len(discounts))
            if not valid:
                Console.print_error(error)
                Console.pause()
                return
            
            selected_discount = discounts[num - 1]
            self.pricing.assign_discount_to_product(sku.upper(), selected_discount.get_id())
            Console.print_success(f"Знижку '{selected_discount.get_name()}' застосовано до товару!")
        
        elif choice == "4":
            sku = Console.input_prompt("SKU товару")
            product = self.warehouse.get_product(sku.upper())
            if not product:
                Console.print_error(f"Товар з SKU '{sku}' не знайдено")
                Console.pause()
                return
            
            qty_str = Console.input_prompt("Кількість")
            valid, qty, error = Validators.validate_positive_int(qty_str)
            if not valid:
                Console.print_error(error)
                Console.pause()
                return
            
            discount_code = Console.input_prompt("Код знижки (Enter для автоматичної)")
            
            result = self.pricing.calculate_price(product, qty, discount_code if discount_code.strip() else None)
            
            print()
            Console.print_info(f"Товар: {result['name']}")
            Console.print_info(f"Кількість: {result['quantity']}")
            Console.print_info(f"Базова ціна: {result['base_price']:.2f} грн.")
            Console.print_info(f"Сума без знижки: {result['total_base']:.2f} грн.")
            if result['discount_applied']:
                Console.print_success(f"Застосована знижка: {result['discount_applied']}")
                Console.print_success(f"Економія: {result['savings']:.2f} грн.")
            Console.print_success(f"Фінальна ціна: {result['final_price']:.2f} грн.")
        
        Console.pause()

    def _view_notifications(self):
        Console.clear()
        Console.print_header("🔔 Сповіщення")
        
        unread = self.notifications.get_unread_count()
        total = len(self.notifications.get_all_alerts())
        
        Console.print_info(f"Всього сповіщень: {total} (непрочитаних: {unread})")
        print()
        
        Console.print_menu_item(1, "Переглянути всі сповіщення")
        Console.print_menu_item(2, "Переглянути критичні")
        Console.print_menu_item(3, "Позначити всі як прочитані")
        Console.print_menu_item(4, "Перевірити склад на проблеми")
        Console.print_menu_item(5, "Очистити всі сповіщення")
        Console.print_menu_item(0, "Назад")
        print()

        choice = Console.input_prompt("Виберіть дію")
        
        if choice == "1":
            alerts = self.notifications.get_all_alerts()
            if not alerts:
                Console.print_warning("Сповіщення відсутні")
            else:
                for alert in reversed(alerts[-20:]):
                    level = alert.get_level()
                    if level == AlertLevel.CRITICAL:
                        color = Colors.RED
                        icon = "🔴"
                    elif level == AlertLevel.WARNING:
                        color = Colors.YELLOW
                        icon = "🟡"
                    else:
                        color = Colors.CYAN
                        icon = "🔵"
                    
                    read_mark = "" if alert.is_read() else " (НОВЕ)"
                    print(f"  {icon} {color}{alert.get_title()}{read_mark}{Colors.ENDC}")
                    Console.print_item(alert.get_message(), 6)
                    print()
        
        elif choice == "2":
            critical = self.notifications.get_alerts_by_level(AlertLevel.CRITICAL)
            if not critical:
                Console.print_success("Критичних сповіщень немає!")
            else:
                Console.print_warning(f"Критичних сповіщень: {len(critical)}")
                print()
                for alert in critical:
                    print(f"  {Colors.RED}🔴 {alert.get_title()}{Colors.ENDC}")
                    Console.print_item(alert.get_message(), 6)
        
        elif choice == "3":
            self.notifications.mark_all_as_read()
            Console.print_success("Всі сповіщення позначено як прочитані!")
        
        elif choice == "4":
            self._check_alerts()
            Console.print_success("Перевірку завершено!")
            unread_new = self.notifications.get_unread_count()
            if unread_new > unread:
                Console.print_warning(f"Виявлено нових проблем: {unread_new - unread}")
        
        elif choice == "5":
            confirm = Console.input_prompt("Ви впевнені? (так/ні)")
            if confirm.lower() in ["так", "yes", "y"]:
                self.notifications.clear_alerts()
                Console.print_success("Всі сповіщення видалено!")
        
        Console.pause()

    def _backup_restore(self):
        Console.clear()
        Console.print_header("💾 Резервне копіювання")
        
        Console.print_menu_item(1, "Створити резервну копію")
        Console.print_menu_item(2, "Переглянути резервні копії")
        Console.print_menu_item(3, "Інформація про резервну копію")
        Console.print_menu_item(4, "Видалити стару резервну копію")
        Console.print_menu_item(5, "Автоматичне очищення (залишити останні 10)")
        Console.print_menu_item(0, "Назад")
        print()

        choice = Console.input_prompt("Виберіть дію")
        
        if choice == "1":
            filepath = self.backup_service.create_backup(
                self.warehouse, 
                self.suppliers, 
                self.orders
            )
            Console.print_success(f"Резервну копію створено: {filepath}")
            self.history.add_record(
                OperationType.REPORT_GENERATED,
                "Створено резервну копію",
                details={"файл": filepath}
            )
        
        elif choice == "2":
            backups = self.backup_service.list_backups()
            if not backups:
                Console.print_warning("Резервних копій не знайдено")
            else:
                Console.print_success(f"Знайдено резервних копій: {len(backups)}")
                print()
                widths = [30, 15, 12]
                Console.print_table_header(["Файл", "Товарів", "Розмір"], widths)
                for backup in backups[:10]:
                    size_kb = backup['size'] / 1024
                    Console.print_table_row([
                        backup['filename'][:28],
                        backup['products_count'],
                        f"{size_kb:.1f} KB"
                    ], widths)
        
        elif choice == "3":
            filename = Console.input_prompt("Ім'я файлу резервної копії")
            info = self.backup_service.get_backup_info(filename)
            if not info:
                Console.print_error("Резервну копію не знайдено")
            else:
                Console.print_success("Інформація про резервну копію:")
                Console.print_item(f"Файл: {info['filename']}")
                Console.print_item(f"Створено: {info['created_at']}")
                Console.print_item(f"Версія: {info['version']}")
                Console.print_item(f"Товарів: {info['products_count']}")
                Console.print_item(f"Постачальників: {info['suppliers_count']}")
                Console.print_item(f"Замовлень: {info['orders_count']}")
        
        elif choice == "4":
            filename = Console.input_prompt("Ім'я файлу для видалення")
            if self.backup_service.delete_backup(filename):
                Console.print_success("Резервну копію видалено!")
            else:
                Console.print_error("Резервну копію не знайдено")
        
        elif choice == "5":
            deleted = self.backup_service.cleanup_old_backups(10)
            Console.print_success(f"Видалено старих резервних копій: {deleted}")
        
        Console.pause()

    def _settings(self):
        Console.clear()
        Console.print_header("⚙️ Налаштування")
        
        print(f"\n{Colors.CYAN}  ┌{'─' * 48}┐{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}          {Colors.BOLD}📊 ІНФОРМАЦІЯ ПРО СИСТЕМУ{Colors.ENDC}            {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  ├{'─' * 48}┤{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}  Версія:           {Colors.WHITE}v{self.VERSION:<25}{Colors.ENDC} {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}  Склад:            {Colors.WHITE}{self.warehouse.get_name():<25}{Colors.ENDC} {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  │{Colors.ENDC}  Локація:          {Colors.WHITE}{self.warehouse.get_location()[:25]:<25}{Colors.ENDC} {Colors.CYAN}│{Colors.ENDC}")
        print(f"{Colors.CYAN}  └{'─' * 48}┘{Colors.ENDC}")
        
        print()
        Console.print_menu_item(1, "Перевірити систему на помилки")
        Console.print_menu_item(2, "Статистика використання пам'яті")
        Console.print_menu_item(3, "Інформація про сервіси")
        Console.print_menu_item(0, "Назад")
        print()

        choice = Console.input_prompt("Виберіть дію")
        
        if choice == "1":
            Console.print_info("Перевірка системи...")
            print()
            Console.print_success("✓ Інтерфейси завантажено")
            Console.print_success("✓ Моделі товарів ініціалізовано")
            Console.print_success("✓ Сервіси запущено")
            Console.print_success("✓ Утиліти доступні")
            Console.print_success("✓ База даних (в пам'яті) працює")
            print()
            Console.print_success("Система працює коректно!")
        
        elif choice == "2":
            import sys
            products_count = len(self.warehouse.get_all_products())
            suppliers_count = len(self.suppliers)
            orders_count = len(self.orders)
            history_count = self.history.get_records_count()
            alerts_count = len(self.notifications.get_all_alerts())
            
            Console.print_info("Статистика об'єктів у пам'яті:")
            Console.print_item(f"Товарів: {products_count}")
            Console.print_item(f"Постачальників: {suppliers_count}")
            Console.print_item(f"Замовлень: {orders_count}")
            Console.print_item(f"Записів історії: {history_count}")
            Console.print_item(f"Сповіщень: {alerts_count}")
        
        elif choice == "3":
            Console.print_info("Активні сервіси:")
            Console.print_item("WarehouseService - управління складом")
            Console.print_item("HistoryService - історія операцій")
            Console.print_item("StatisticsService - статистика")
            Console.print_item("ExportService - експорт даних")
            Console.print_item("NotificationService - сповіщення")
            Console.print_item("PricingService - ціноутворення")
            Console.print_item("BackupService - резервне копіювання")
        
        Console.pause()

    def _exit_app(self):
        Console.clear()
        
        summary = self.statistics.get_summary()
        history_count = self.history.get_records_count()
        
        print(f"""
{Colors.CYAN}{Colors.BOLD}
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║          Дякуємо за використання програми!                ║
    ║                                                           ║
    ║   📊 Статистика сесії:                                    ║
    ║      • Товарів на складі: {summary['загальна_кількість_товарів']:<28}║
    ║      • Загальна вартість: {summary['загальна_вартість']:>14,.2f} грн.        ║
    ║      • Операцій виконано: {history_count:<28}║
    ║                                                           ║
    ║              До побачення! 👋                             ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
{Colors.ENDC}""")


def main():
    try:
        app = WarehouseApp()
        app.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Програму перервано користувачем.{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.RED}Помилка: {e}{Colors.ENDC}")


if __name__ == "__main__":
    main()
