from video.video import Video
from googleapiclient.http import MediaFileUpload


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
