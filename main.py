import os
import sys

from config.config import Config
from utils.functions import get_json, get_thumbnail, get_playlist, mock_upload
from video.filename_processor import FileNameProcessor
from video.filename_schema import FileNameSchema
from video.video import get_video_list, Video, VideoStatus
from youtube.credentials import get_credentials
from youtube.youtube import get_playlists, upload_video, set_thumbnail, attach_to_playlist
from playlists import Playlist

from googleapiclient.discovery import build


# Prepare resources
try:
    config: Config = Config.from_json(get_json('config.json'))
except RuntimeError as exc:
    raise SystemExit(f"Error when handling config file: {exc}") from exc

try:
    filename_schema: FileNameSchema = FileNameSchema.from_json(config.filename_schema)
except Exception as exc:
    raise SystemExit(f"Error when processing filename schema: {exc}") from exc

filename_processor: FileNameProcessor = FileNameProcessor(filename_schema)

youtube_service = build(config.api_service_name, config.api_version, credentials=get_credentials(config))

# Get list of videos in upload directory
try:
    videos: list[Video] = get_video_list(config.videos_path, filename_processor)
except RuntimeError as exc:
    raise SystemExit(exc)

# Get list of playlists from youtube
playlists: list[Playlist] = [Playlist(playlist["id"],
                                      playlist["snippet"]["title"])
                             for playlist
                             in get_playlists(youtube_service, config.playlist)]

for video in videos:
    print(f"Processing video: {video.filename}")
    video.process_filename()
    try:
        video.thumbnail_path = get_thumbnail(config.thumbnails_path, video.related_subject)
    except Exception as exc:
        print(exc, file=sys.stderr)
    try:
        video.playlist = get_playlist(playlists, video.related_subject)
    except Exception as exc:
        print(exc, file=sys.stderr)

    try:
        upload_video(video, youtube_service, config.upload)
    except Exception as exc:
        print(f"Error when uploading video: {exc}", file=sys.stderr)
    else:
        success: bool = False
        tries: int = 0
        while not success or tries < config.thumbnail_tries:
            try:
                set_thumbnail(youtube_service, video.thumbnail_path, video. youtube_id)
                success = True
            except Exception as exc:
                print(f"Error setting thumbnail: {exc}", file=sys.stderr)
            tries = tries + 1
        success = False
        tries = 0
        while not success or tries < config.playlist_tries:
            try:
                attach_to_playlist(youtube_service, video.playlist.youtube_id, video.youtube_id)
                success = True
            except Exception as exc:
                print(f"Error attaching to playlist: {exc}", file=sys.stderr)
            tries = tries + 1
    if video.status == VideoStatus.UPLOADED:
        os.remove(video.path)
        video.status = VideoStatus.DELETED

