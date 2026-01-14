import googleapiclient.discovery
from liker import get_authenticated_service, get_channel_videos, like_videos


def get_channel_id(youtube, username):
    request = youtube.channels().list(
        part="id",
        forUsername=username
    )
    response = request.execute()
    channel = response.get("items", [])[0]

    return channel["id"] if channel else None


def main():
    youtube = get_authenticated_service()

    # Replace 'CHANNEL_USERNAME' with the username of the channel you want to fetch all videos from.
    channel_username = "@the_hampter"
    channel_id = get_channel_id(youtube, channel_username)

    if channel_id:
        print(f"Channel ID found: {channel_id}")
        print("Fetching all videos from the channel...")
        video_ids = get_channel_videos(youtube, channel_id)
        print(f"Found {len(video_ids)} videos.")

        print("Starting to like all videos...")
        like_videos(youtube, video_ids)
        print("Finished liking all videos!")
    else:
        print("Channel ID not found for the given username.")


if __name__ == "__main__":
    main()