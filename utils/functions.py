import json

from typing import Optional


def get_json(path: str) -> Optional[dict]:
    try:
        with open(file=path, encoding="Utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError as exc:
        raise RuntimeError("Json file not found.") from exc
    except Exception as exc:
        raise RuntimeError(exc) from exc