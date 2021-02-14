from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional

from utils.json_parser import JsonParser


@dataclass
class ItemDescriptor(JsonParser):
    name: str
    required: bool
    prefix: str = ''
    suffix: str = ''


@dataclass
class FileNameSchema(JsonParser):
    separator: str
    items: list[ItemDescriptor]
    change: dict[str, str] = field(default_factory=dict)

    def get_item_position(self, item_name: str) -> Optional[int]:
        for i, item in enumerate(self.items):
            if item.name == item_name:
                return i

