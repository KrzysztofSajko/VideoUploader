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

        initializer: dict = {}

        for key, val in cls.__dataclass_fields__.items():
            if key in json:
                is_list: bool = type(get_origin(get_type_hints(cls)[key])) == type(list)
                args = get_args(get_type_hints(cls)[key])
                inner_type = args[0] if len(args) > 0 else None
                is_from_this_module: bool = inner_type and inner_type.__module__ == cls.__module__
                if is_list and is_from_this_module:
                    initializer[key] = []
                    for i, element in enumerate(json[key]):
                        try:
                            initializer[key].append(inner_type.from_json(element))
                        except Exception as exc:
                            raise Exception(f"Error when processing {i} item: {exc}") from exc
                else:
                    initializer[key] = json[key]
            else:
                if is_required(val):
                    raise KeyError(f"Json passed to {cls.__name__} does not contain required key: \"{key}\"")
        return cls(**initializer)