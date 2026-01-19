from abc import ABC, abstractmethod
from typing import List
from datetime import datetime


class IReport(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass

    @abstractmethod
    def get_report_type(self) -> str:
        pass

    @abstractmethod
    def get_generated_date(self) -> datetime:
        pass

    @abstractmethod
    def export_to_dict(self) -> dict:
        pass
