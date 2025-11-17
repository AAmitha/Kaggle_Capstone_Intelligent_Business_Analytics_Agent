"""Memory Bank for long-term storage of insights and preferences."""

import json
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class MemoryEntry:
    """Represents a memory entry."""
    key: str
    value: str
    category: str  # "insight", "preference", "fact", etc.
    timestamp: datetime
    metadata: Dict = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


class MemoryBank:
    """Long-term memory storage for agent insights and user preferences."""
    
    def __init__(self, storage_path: Optional[str] = None):
        self.storage_path = Path(storage_path) if storage_path else Path("data/memory_bank.json")
        self.memories: Dict[str, MemoryEntry] = {}
        self._load_memories()
    
    def store(self, key: str, value: str, category: str = "general", metadata: Optional[Dict] = None):
        """Store a memory entry."""
        entry = MemoryEntry(
            key=key,
            value=value,
            category=category,
            timestamp=datetime.now(),
            metadata=metadata or {}
        )
        self.memories[key] = entry
        self._save_memories()
    
    def retrieve(self, key: str) -> Optional[str]:
        """Retrieve a memory entry by key."""
        entry = self.memories.get(key)
        return entry.value if entry else None
    
    def search(self, category: Optional[str] = None, query: Optional[str] = None) -> List[MemoryEntry]:
        """Search memories by category or query."""
        results = []
        for entry in self.memories.values():
            if category and entry.category != category:
                continue
            if query and query.lower() not in entry.value.lower():
                continue
            results.append(entry)
        return results
    
    def get_user_preferences(self, user_id: str) -> Dict:
        """Get user preferences from memory."""
        preferences = {}
        for entry in self.memories.values():
            if entry.category == "preference" and entry.metadata.get("user_id") == user_id:
                preferences[entry.key] = entry.value
        return preferences
    
    def store_insight(self, insight: str, metadata: Optional[Dict] = None):
        """Store an insight with auto-generated key."""
        key = f"insight_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.store(key, insight, category="insight", metadata=metadata)
        return key
    
    def _load_memories(self):
        """Load memories from disk."""
        if not self.storage_path.exists():
            return
        
        try:
            with open(self.storage_path, 'r') as f:
                data = json.load(f)
                for key, entry_data in data.items():
                    # Convert timestamp string back to datetime
                    entry_data['timestamp'] = datetime.fromisoformat(entry_data['timestamp'])
                    self.memories[key] = MemoryEntry(**entry_data)
        except Exception as e:
            print(f"Error loading memories: {e}")
    
    def _save_memories(self):
        """Save memories to disk."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            data = {}
            for key, entry in self.memories.items():
                entry_dict = asdict(entry)
                entry_dict['timestamp'] = entry.timestamp.isoformat()
                data[key] = entry_dict
            
            with open(self.storage_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving memories: {e}")

