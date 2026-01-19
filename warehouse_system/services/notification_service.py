from datetime import datetime
from typing import List, Callable, Optional
from enum import Enum


class AlertLevel(Enum):
    INFO = "Інформація"
    WARNING = "Попередження"
    CRITICAL = "Критично"


class Alert:
    def __init__(self, level: AlertLevel, title: str, message: str, source: str = "Система"):
        self._id = datetime.now().strftime("%Y%m%d%H%M%S%f")
        self._timestamp = datetime.now()
        self._level = level
        self._title = title
        self._message = message
        self._source = source
        self._is_read = False

    def get_id(self) -> str:
        return self._id

    def get_timestamp(self) -> datetime:
        return self._timestamp

    def get_level(self) -> AlertLevel:
        return self._level

    def get_title(self) -> str:
        return self._title

    def get_message(self) -> str:
        return self._message

    def get_source(self) -> str:
        return self._source

    def is_read(self) -> bool:
        return self._is_read

    def mark_as_read(self):
        self._is_read = True

    def to_dict(self) -> dict:
        return {
            "id": self._id,
            "timestamp": self._timestamp.isoformat(),
            "level": self._level.value,
            "title": self._title,
            "message": self._message,
            "source": self._source,
            "is_read": self._is_read
        }

    def __str__(self) -> str:
        status = "○" if not self._is_read else "●"
        time_str = self._timestamp.strftime("%d.%m %H:%M")
        return f"{status} [{time_str}] {self._level.value}: {self._title}"


class NotificationService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._alerts: List[Alert] = []
            cls._instance._subscribers: List[Callable] = []
        return cls._instance

    def add_alert(self, level: AlertLevel, title: str, message: str, source: str = "Система") -> Alert:
        alert = Alert(level, title, message, source)
        self._alerts.append(alert)
        self._notify_subscribers(alert)
        return alert

    def info(self, title: str, message: str, source: str = "Система") -> Alert:
        return self.add_alert(AlertLevel.INFO, title, message, source)

    def warning(self, title: str, message: str, source: str = "Система") -> Alert:
        return self.add_alert(AlertLevel.WARNING, title, message, source)

    def critical(self, title: str, message: str, source: str = "Система") -> Alert:
        return self.add_alert(AlertLevel.CRITICAL, title, message, source)

    def get_all_alerts(self) -> List[Alert]:
        return self._alerts.copy()

    def get_unread_alerts(self) -> List[Alert]:
        return [a for a in self._alerts if not a.is_read()]

    def get_alerts_by_level(self, level: AlertLevel) -> List[Alert]:
        return [a for a in self._alerts if a.get_level() == level]

    def get_recent_alerts(self, count: int = 10) -> List[Alert]:
        return self._alerts[-count:] if self._alerts else []

    def get_unread_count(self) -> int:
        return len(self.get_unread_alerts())

    def mark_all_as_read(self):
        for alert in self._alerts:
            alert.mark_as_read()

    def mark_as_read(self, alert_id: str) -> bool:
        for alert in self._alerts:
            if alert.get_id() == alert_id:
                alert.mark_as_read()
                return True
        return False

    def clear_alerts(self):
        self._alerts.clear()

    def subscribe(self, callback: Callable):
        self._subscribers.append(callback)

    def unsubscribe(self, callback: Callable):
        if callback in self._subscribers:
            self._subscribers.remove(callback)

    def _notify_subscribers(self, alert: Alert):
        for subscriber in self._subscribers:
            try:
                subscriber(alert)
            except Exception:
                pass

    def check_low_stock(self, warehouse, threshold: int = 10):
        low_stock = warehouse.get_low_stock_products(threshold)
        for product in low_stock:
            qty = product.get_quantity()
            if qty <= 3:
                self.critical(
                    f"Критично низький запас: {product.get_name()}",
                    f"Залишилось лише {qty} од. товару {product.get_sku()}",
                    "Моніторинг запасів"
                )
            elif qty <= threshold:
                self.warning(
                    f"Низький запас: {product.get_name()}",
                    f"Залишилось {qty} од. товару {product.get_sku()}",
                    "Моніторинг запасів"
                )

    def check_expiring_products(self, warehouse, days_threshold: int = 7):
        from datetime import date, timedelta
        products = warehouse.get_all_products()
        today = date.today()
        
        for product in products:
            if hasattr(product, 'get_expiration_date'):
                exp_date = product.get_expiration_date()
                days_left = (exp_date - today).days
                
                if days_left < 0:
                    self.critical(
                        f"Прострочений товар: {product.get_name()}",
                        f"Термін придатності закінчився {abs(days_left)} днів тому",
                        "Контроль якості"
                    )
                elif days_left <= days_threshold:
                    self.warning(
                        f"Закінчується термін: {product.get_name()}",
                        f"Залишилось {days_left} днів до закінчення терміну придатності",
                        "Контроль якості"
                    )
