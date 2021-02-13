from __future__ import annotations
from dataclasses import dataclass, field
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

