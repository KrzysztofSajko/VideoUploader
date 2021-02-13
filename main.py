import os

from googleapiclient.http import MediaFileUpload

from config.config import Config
from video.filename_processor import FileNameProcessor
from video.filename_schema import FileNameSchema
from video.video import Video
from utils.functions import get_json


def get_video_list(videos_path: str, filename_processor: FileNameProcessor):
    if os.path.isdir(videos_path):
        return [Video(os.path.join(videos_path, path),
                      path.split('.')[0],
                      filename_processor)
                for path
                in os.listdir(videos_path)
                if os.path.isfile(os.path.join(videos_path, path))]
    raise RuntimeError(f'Video directory: "{os.path.abspath(videos_path)}" does not exist.')


def upload_video(video: Video, youtube_service):
    request = youtube_service.videos().insert(
        part="snippet,status",
        body={
            "snippet": {
                "categoryId": "22",
                "description": "Description of uploaded video.",
                "title": "Test video upload."
            },
            "status": {
                "privacyStatus": "private",
                "madeForKids": False
            }
        },
        media_body=MediaFileUpload(video.path, chunksize=-1, resumable=True)
    )
    response = request.execute()
    video.youtube_id = response["id"]


try:
    config = Config.from_json(get_json('config.json'))
except RuntimeError as exc:
    raise SystemExit(f"Error when handling config file: {exc}") from exc

print(config)

try:
    filename_schema: FileNameSchema = FileNameSchema.from_json(config.filename_schema)
except Exception as exc:
    raise SystemExit(f"Error when processing filename schema: {exc}") from exc

filename_processor = FileNameProcessor(filename_schema)

try:
    videos = get_video_list(config.videos_path, filename_processor)
except RuntimeError as exc:
    raise SystemExit(exc)

for video in videos:
    video.process_filename()
    print(video.title)

# youtube_service = build(config.api_service_name, config.api_version, credentials=get_credentials(config))