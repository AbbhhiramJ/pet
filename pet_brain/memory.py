import json
from pathlib import Path
from typing import Any

class LocalMemory:
    """Tiny append-only JSON memory store for the development phase."""
    def __init__(self, path: str | Path = "data/memory.json", limit: int = 50) -> None:
        self.path = Path(path)
        self.limit = limit
        self.entries: list[dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if not self.path.exists():
            return
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return
        if isinstance(data, list):
            self.entries = [item for item in data if isinstance(item, dict)][-self.limit:]

    def add(self, role: str, content: str) -> None:
        self.entries.append({"role": role, "content": content})
        self.entries = self.entries[-self.limit:]
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps(self.entries, indent=2), encoding="utf-8")

    def recent(self, count: int = 8) -> list[dict[str, Any]]:
        return self.entries[-count:]
