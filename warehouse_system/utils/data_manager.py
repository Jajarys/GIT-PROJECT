import json
import os
from datetime import datetime
from typing import Dict, Any


class DataManager:
    def __init__(self, data_dir: str = "data"):
        self._data_dir = data_dir
        self._ensure_data_dir()

    def _ensure_data_dir(self):
        if not os.path.exists(self._data_dir):
            os.makedirs(self._data_dir)

    def _get_filepath(self, filename: str) -> str:
        return os.path.join(self._data_dir, filename)

    def save_json(self, filename: str, data: Dict[str, Any]) -> bool:
        try:
            filepath = self._get_filepath(filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
            return True
        except Exception:
            return False

    def load_json(self, filename: str) -> Dict[str, Any]:
        try:
            filepath = self._get_filepath(filename)
            if os.path.exists(filepath):
                with open(filepath, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}

    def save_report(self, report_type: str, content: str) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"report_{report_type}_{timestamp}.txt"
        filepath = self._get_filepath(filename)
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return filepath
        except Exception:
            return ""

    def list_reports(self) -> list:
        try:
            files = os.listdir(self._data_dir)
            return [f for f in files if f.startswith("report_") and f.endswith(".txt")]
        except Exception:
            return []

    def delete_file(self, filename: str) -> bool:
        try:
            filepath = self._get_filepath(filename)
            if os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception:
            pass
        return False
