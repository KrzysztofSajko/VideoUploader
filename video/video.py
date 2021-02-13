from dataclasses import dataclass
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
    description: str = None
    playlist: str = None
    thumbnail_path: str = None
    youtube_id: str = None
    status: VideoStatus = VideoStatus.FOUND

    def process_filename(self):
        self.title = self.filename_processor.get_title(self.filename)
