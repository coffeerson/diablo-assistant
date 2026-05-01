import json
import uuid
from datetime import datetime
from pathlib import Path


class FavoritesManager:
    def __init__(self, data_file="favorites.json"):
        self.data_file = Path(__file__).parent / data_file
        self._ensure_file()

    def _ensure_file(self):
        if not self.data_file.exists():
            self.save([])

    def load(self) -> list[dict]:
        with open(self.data_file, "r", encoding="utf-8") as f:
            return json.load(f)

    def save(self, data: list[dict]) -> None:
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_all(self) -> list[dict]:
        return self.load()

    def add(self, name: str, url: str) -> dict:
        data = self.load()
        item = {
            "id": str(uuid.uuid4())[:8],
            "name": name,
            "url": url,
            "added_at": datetime.now().isoformat(),
        }
        data.append(item)
        self.save(data)
        return item

    def update(self, item_id: str, name: str, url: str) -> bool:
        data = self.load()
        for item in data:
            if item["id"] == item_id:
                item["name"] = name
                item["url"] = url
                self.save(data)
                return True
        return False

    def delete(self, item_id: str) -> bool:
        data = self.load()
        new_data = [item for item in data if item["id"] != item_id]
        if len(new_data) != len(data):
            self.save(new_data)
            return True
        return False
