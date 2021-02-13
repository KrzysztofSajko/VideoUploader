import os
import json

def get_config():
    try:
        with open(file="config.json", encoding="Utf-8") as config_file:
            return json.load(config_file)
    except FileNotFoundError as exc:
        raise RuntimeError("Config file not found.") from exc

try:
    config = get_config()
except RuntimeError as exc:
    raise SystemExit(f"Error when opening config file: {exc}")

print(config)