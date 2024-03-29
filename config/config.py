from dataclasses import dataclass
from utils.json_parser import JsonParser


@dataclass
class Config(JsonParser):
    videos_path: str
    thumbnails_path: str
    port: int
    api_service_name: str
    api_version: str
    client_secrets_file: str
    token_path: str
    scopes: list[str]
    filename_schema: dict
    playlist: dict
    upload: dict
    thumbnail_tries: int
    playlist_tries: int
