# youtube_uploader.py

import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

def upload_to_youtube(video_file, title, description, tags, category="22", privacy_status="public"):
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]

    # Disable OAuthlib's HTTPS verification when running locally.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    # Get credentials and create an API client
    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secrets.json"  # Path to your client secrets file

    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    # Upload the video
    media_file = googleapiclient.http.MediaFileUpload(video_file)
    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )
    response = request.execute()
    return response
