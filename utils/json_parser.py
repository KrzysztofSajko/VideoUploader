from __future__ import annotations
from dataclasses import _MISSING_TYPE
from typing import get_args, get_origin, get_type_hints, TypeVar, Optional
from abc import ABC


T = TypeVar('T', bound='JsonParser')


class JsonParser(ABC):
    @classmethod
    def from_json(cls, json: dict) -> Optional[T]:
        def is_required(value) -> bool:
            return type(value.default) == _MISSING_TYPE and type(value.default_factory) == _MISSING_TYPE

        def is_list(field) -> bool:
            return type(get_origin(get_type_hints(cls)[field])) == type(list)

        def is_from_this_module(type) -> bool:
            return type and type.__module__ == cls.__module__

        initializer: dict = {}

        for field, value in cls.__dataclass_fields__.items():
            if field in json:
                inner_types = get_args(get_type_hints(cls)[field])
                inner_type = inner_types[0] if len(inner_types) > 0 else None
                if is_list(field) and is_from_this_module(inner_type):
                    initializer[field] = []
                    for i, element in enumerate(json[field]):
                        try:
                            initializer[field].append(inner_type.from_json(element))
                        except Exception as exc:
                            raise Exception(f"Error when processing {i} item: {exc}") from exc
                else:
                    initializer[field] = json[field]
            else:
                if is_required(value):
                    raise KeyError(f"Json passed to {cls.__name__} does not contain required key: \"{field}\"")
        return cls(**initializer)
