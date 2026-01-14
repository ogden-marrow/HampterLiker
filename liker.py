import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from google.oauth2.credentials import Credentials

# Get your OAuth 2.0 client secrets file from the Google Developer Console

client_secrets_file = "client_secret_308678656389-9iggfmqfvbh3rh2d5ssg5l4k99fu2468.apps.googleusercontent.com.json"

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
api_service_name = "youtube"
api_version = "v3"


def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)


def get_channel_videos(youtube, channel_id):
    all_videos = []
    next_page_token = None

    while True:
        request = youtube.search().list(
            part="id",
            channelId=channel_id,
            maxResults=50,
            pageToken=next_page_token,
            type="video"
        )
        response = request.execute()
        videos = [item["id"]["videoId"] for item in response["items"]]
        all_videos.extend(videos)

        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break

    return all_videos


def like_videos(youtube, video_ids):
    for video_id in video_ids:
        try:
            youtube.videos().rate(id=video_id, rating="like").execute()
            print(f"Video '{video_id}' liked.")
        except googleapiclient.errors.HttpError as error:
            print(f"An error occurred: {error}")
            print(f"Video '{video_id}' could not be liked.")


def main():
    youtube = get_authenticated_service()

    # Replace 'CHANNEL_ID' with the ID of the channel you want to like all videos from.
    channel_id = "CHANNEL_ID"
    video_ids = get_channel_videos(youtube, channel_id)

    like_videos(youtube, video_ids)


if __name__ == "__main__":
    main()
