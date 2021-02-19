from video.video import Video, VideoStatus
from googleapiclient.http import MediaFileUpload


def upload_video(video: Video, youtube_service, upload_config: dict):
    body: dict = {
        "snippet": {
            "description": video.description,
            "title": video.title
        }
    }

    for key, value in upload_config["body"].items():
        if key in body:
            body[key] = {**body[key], **value}
        else:
            body[key] = value

    response = youtube_service.videos().insert(
        part=upload_config["part"],
        body=body,
        media_body=MediaFileUpload(video.path)
    ).execute()

    # print(response)

    if "id" in response:
        video.youtube_id = response["id"]
        video.status = VideoStatus.UPLOADED
    else:
        raise Exception("Failed to upload video")


def get_playlists(youtube_service, playlist_config: dict):
    playlists: list = []
    response = None
    page_token = None
    while response is None or "nextPageToken" in response:
        response = youtube_service.playlists().list(
            pageToken=page_token,
            **playlist_config
        ).execute()
        if "items" in response:
            playlists = [*playlists, *response["items"]]
        if "nextPageToken" in response:
            page_token = response["nextPageToken"]
    return playlists


def set_thumbnail(youtube_service, thumbnail_path: str, video_id: str):
    response = youtube_service.thumbnails().set(
        videoId=video_id,
        media_body=MediaFileUpload(thumbnail_path, chunksize=-1, resumable=True)
    ).execute()
    # print(response)


def attach_to_playlist(youtube_service, playlist_id: str, video_id: str):
    response = youtube_service.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
                "playlistId": playlist_id,
                "position": 0,
                "resourceId": {
                    "kind": "youtube#video",
                    "videoId": video_id
                }
            }
        }
    ).execute()
    # print(response)
