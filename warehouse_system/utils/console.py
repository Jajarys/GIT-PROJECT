import os
import sys


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE = '\033[97m'
    MAGENTA = '\033[35m'


class Console:
    @staticmethod
    def init():
        if sys.platform == 'win32':
            os.system('color')
            os.system('chcp 65001 >nul 2>&1')

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def print_header(text: str):
        print(f"\n{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.WHITE}  {text.upper()}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.CYAN}{'═' * 60}{Colors.ENDC}\n")

    @staticmethod
    def print_subheader(text: str):
        print(f"\n{Colors.YELLOW}{'─' * 50}{Colors.ENDC}")
        print(f"{Colors.BOLD}{Colors.YELLOW}  {text}{Colors.ENDC}")
        print(f"{Colors.YELLOW}{'─' * 50}{Colors.ENDC}")

    @staticmethod
    def print_success(text: str):
        print(f"{Colors.GREEN}✓ {text}{Colors.ENDC}")

    @staticmethod
    def print_error(text: str):
        print(f"{Colors.RED}✗ {text}{Colors.ENDC}")

    @staticmethod
    def print_warning(text: str):
        print(f"{Colors.YELLOW}⚠ {text}{Colors.ENDC}")

    @staticmethod
    def print_info(text: str):
        print(f"{Colors.CYAN}ℹ {text}{Colors.ENDC}")

    @staticmethod
    def print_item(text: str, indent: int = 2):
        print(f"{' ' * indent}{Colors.WHITE}• {text}{Colors.ENDC}")

    @staticmethod
    def print_menu_item(number: int, text: str):
        print(f"  {Colors.CYAN}[{number}]{Colors.ENDC} {Colors.WHITE}{text}{Colors.ENDC}")

    @staticmethod
    def print_table_header(columns: list, widths: list):
        header = ""
        for col, width in zip(columns, widths):
            header += f"{Colors.BOLD}{Colors.CYAN}{col:<{width}}{Colors.ENDC}"
        print(header)
        print(f"{Colors.CYAN}{'─' * sum(widths)}{Colors.ENDC}")

    @staticmethod
    def print_table_row(values: list, widths: list):
        row = ""
        for val, width in zip(values, widths):
            row += f"{Colors.WHITE}{str(val):<{width}}{Colors.ENDC}"
        print(row)

    @staticmethod
    def input_prompt(text: str) -> str:
        return input(f"{Colors.GREEN}► {text}: {Colors.ENDC}")

    @staticmethod
    def pause():
        input(f"\n{Colors.CYAN}Натисніть Enter для продовження...{Colors.ENDC}")
