from typing import Optional, Tuple
from datetime import date


class Validators:
    @staticmethod
    def validate_positive_int(value: str) -> Tuple[bool, Optional[int], str]:
        try:
            num = int(value)
            if num <= 0:
                return False, None, "Значення повинно бути більше 0"
            return True, num, ""
        except ValueError:
            return False, None, "Введіть ціле число"

    @staticmethod
    def validate_positive_float(value: str) -> Tuple[bool, Optional[float], str]:
        try:
            num = float(value)
            if num <= 0:
                return False, None, "Значення повинно бути більше 0"
            return True, num, ""
        except ValueError:
            return False, None, "Введіть число"

    @staticmethod
    def validate_non_empty(value: str) -> Tuple[bool, str, str]:
        if not value or not value.strip():
            return False, "", "Поле не може бути порожнім"
        return True, value.strip(), ""

    @staticmethod
    def validate_sku(value: str) -> Tuple[bool, str, str]:
        value = value.strip().upper()
        if not value:
            return False, "", "SKU не може бути порожнім"
        if len(value) < 3:
            return False, "", "SKU повинен містити мінімум 3 символи"
        return True, value, ""

    @staticmethod
    def validate_date(value: str) -> Tuple[bool, Optional[date], str]:
        try:
            parts = value.split('.')
            if len(parts) != 3:
                return False, None, "Формат дати: ДД.ММ.РРРР"
            day, month, year = int(parts[0]), int(parts[1]), int(parts[2])
            result_date = date(year, month, day)
            return True, result_date, ""
        except (ValueError, IndexError):
            return False, None, "Невірний формат дати. Використовуйте ДД.ММ.РРРР"

    @staticmethod
    def validate_email(value: str) -> Tuple[bool, str, str]:
        value = value.strip()
        if '@' not in value or '.' not in value:
            return False, "", "Невірний формат електронної пошти"
        return True, value, ""

    @staticmethod
    def validate_phone(value: str) -> Tuple[bool, str, str]:
        value = value.strip().replace(' ', '').replace('-', '')
        if not value.startswith('+'):
            value = '+' + value
        digits = ''.join(c for c in value if c.isdigit())
        if len(digits) < 10:
            return False, "", "Номер телефону повинен містити мінімум 10 цифр"
        return True, value, ""

    @staticmethod
    def validate_menu_choice(value: str, min_val: int, max_val: int) -> Tuple[bool, Optional[int], str]:
        try:
            choice = int(value)
            if choice < min_val or choice > max_val:
                return False, None, f"Виберіть опцію від {min_val} до {max_val}"
            return True, choice, ""
        except ValueError:
            return False, None, "Введіть номер опції"
