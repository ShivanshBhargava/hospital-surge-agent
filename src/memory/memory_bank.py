# src/memory/session_store.py
# src/memory/memory_bank.py
import json
from typing import List, Dict
import os

MEMORY_FILE = "data/memory.json"

class MemoryBank:
    """
    Stores and retrieves past surge events and their outcomes.
    """

    def __init__(self):
        if not os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "w") as f:
                json.dump([], f)
        self._load()

    def _load(self):
        with open(MEMORY_FILE) as f:
            self.memories: List[Dict] = json.load(f)

    def save(self):
        with open(MEMORY_FILE, "w") as f:
            json.dump(self.memories, f, indent=2)

    def add_memory(self, entry: Dict):
        self.memories.append(entry)
        self.save()

    def retrieve_related(self, context: str, max_items=3) -> List[Dict]:
        """
        Naive semantic match: prioritizes memories that share keywords with context.
        """
        context = context.lower()
        ranked = sorted(
            self.memories,
            key=lambda m: sum(1 for k in m.get("tags", []) if k.lower() in context),
            reverse=True,
        )
        return ranked[:max_items]
