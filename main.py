import sys

from config.config import Config
from utils.functions import get_json, get_thumbnail, get_playlist
from video.filename_processor import FileNameProcessor
from video.filename_schema import FileNameSchema
from video.video import get_video_list, Video
from youtube.credentials import get_credentials
from youtube.youtube import get_playlists
from playlists import Playlist

from googleapiclient.discovery import build

try:
    config: Config = Config.from_json(get_json('config.json'))
except RuntimeError as exc:
    raise SystemExit(f"Error when handling config file: {exc}") from exc

try:
    filename_schema: FileNameSchema = FileNameSchema.from_json(config.filename_schema)
except Exception as exc:
    raise SystemExit(f"Error when processing filename schema: {exc}") from exc

filename_processor: FileNameProcessor = FileNameProcessor(filename_schema)

try:
    videos: list[Video] = get_video_list(config.videos_path, filename_processor)
except RuntimeError as exc:
    raise SystemExit(exc)

for video in videos:
    video.process_filename()
    try:
        video.thumbnail_path = get_thumbnail(config.thumbnails_path, video.related_subject)
    except Exception as exc:
        print(exc, file=sys.stderr)
    print(video.related_subject, video.thumbnail_path)

youtube_service = build(config.api_service_name, config.api_version, credentials=get_credentials(config))
playlists: list[Playlist] = [Playlist(playlist["id"], playlist["snippet"]["title"]) for playlist in get_playlists(youtube_service, config.playlist)]

for video in videos:
    video.playlist = get_playlist(playlists, video.related_subject).youtube_id
    print(video)
