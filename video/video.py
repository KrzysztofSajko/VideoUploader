import os
from dataclasses import dataclass
from typing import Optional

from playlists import Playlist
from .filename_processor import FileNameProcessor
from enum import Enum, auto


class VideoStatus(Enum):
    FOUND = auto()
    UPLOADED = auto()
    DELETED = auto()


@dataclass
class Video:
    path: str
    filename: str
    filename_processor: FileNameProcessor
    title: str = None
    description: str = ""
    playlist: Playlist = None
    thumbnail_path: str = None
    youtube_id: str = None
    status: VideoStatus = VideoStatus.FOUND

    def process_filename(self):
        self.title = self.filename_processor.get_title(self.filename)

    @property
    def related_subject(self) -> Optional[str]:
        return self.filename_processor.get_item(self.filename, "subject")


def get_video_list(videos_path: str, filename_processor: FileNameProcessor):
    if os.path.isdir(videos_path):
        return [Video(os.path.join(videos_path, path),
                      path.split('.')[0],
                      filename_processor)
                for path
                in os.listdir(videos_path)
                if os.path.isfile(os.path.join(videos_path, path))]
    raise RuntimeError(f'Video directory: "{os.path.abspath(videos_path)}" does not exist.')
