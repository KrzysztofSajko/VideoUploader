import json
import os

from typing import Optional

from playlists import Playlist


def get_json(path: str) -> Optional[dict]:
    try:
        with open(file=path, encoding="Utf-8") as json_file:
            return json.load(json_file)
    except FileNotFoundError as exc:
        raise RuntimeError("Json file not found.") from exc
    except Exception as exc:
        raise RuntimeError(exc) from exc


def get_thumbnail(thumbnails_path: str, subject: str) -> str:
    matches: list = []
    for path, dirs, files in os.walk(thumbnails_path):
        matches = [*matches, *[os.path.join(path, file) for file in files if file.startswith(subject)]]
    if matches:
        return matches[0]
    else:
        raise FileNotFoundError(f"Could not find thumbnail for {subject}"
                                f" in provided directory {os.path.abspath(thumbnails_path)}")


def get_playlist(playlists: list[Playlist], subject: str) -> Optional[Playlist]:
    matches = [playlist for playlist in playlists if subject in playlist.title]
    if matches:
        return matches[0]
