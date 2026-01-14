"""YouTube service layer with functional programming principles."""

from typing import List, Optional, Dict, Any, Callable
from dataclasses import dataclass
from functools import reduce
import glob
import logging

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from config import YouTubeConfig


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Channel:
    """Immutable channel data structure."""

    id: str
    handle: str


@dataclass(frozen=True)
class Video:
    """Immutable video data structure."""

    id: str


@dataclass(frozen=True)
class LikeResult:
    """Immutable result of a like operation."""

    video_id: str
    success: bool
    error: Optional[str] = None
    quota_exceeded: bool = False


# Pure functions for file operations
def find_client_secret_files() -> List[str]:
    """
    Find all client secret files in the current directory.

    Returns:
        List of client secret file paths

    Raises:
        FileNotFoundError: If no client secret files found
    """
    files = glob.glob("client_secret_*.json")
    if not files:
        raise FileNotFoundError(
            "No client_secret_*.json file found in the current directory. "
            "Please download your OAuth 2.0 credentials from Google Cloud Console."
        )
    return files


def get_first_client_secret() -> str:
    """
    Get the first available client secret file.

    Returns:
        Path to the first client secret file
    """
    files = find_client_secret_files()
    client_secret = files[0]
    logger.info(f"Using credentials file: {client_secret}")
    return client_secret


# Authentication functions
def create_authenticated_service(
    client_secrets_file: str,
    config: YouTubeConfig
) -> Any:
    """
    Create an authenticated YouTube service.

    Args:
        client_secrets_file: Path to client secrets JSON file
        config: YouTube API configuration

    Returns:
        Authenticated YouTube service object
    """
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file,
        config.scopes
    )
    credentials = flow.run_local_server(port=0)

    return googleapiclient.discovery.build(
        config.api_service_name,
        config.api_version,
        credentials=credentials
    )


def get_authenticated_service(config: YouTubeConfig) -> Any:
    """
    Get authenticated YouTube service with default client secret.

    Args:
        config: YouTube API configuration

    Returns:
        Authenticated YouTube service object
    """
    client_secret = get_first_client_secret()
    return create_authenticated_service(client_secret, config)


# Channel lookup functions
def lookup_channel_by_handle(
    youtube: Any,
    handle: str
) -> Optional[Dict[str, Any]]:
    """
    Look up channel by handle (e.g., @the_hampter).

    Args:
        youtube: Authenticated YouTube service
        handle: Channel handle without @ symbol

    Returns:
        Channel data dict or None if not found
    """
    try:
        request = youtube.channels().list(part="id", forHandle=handle)
        response = request.execute()
        items = response.get("items", [])
        return items[0] if items else None
    except Exception as e:
        logger.debug(f"forHandle lookup failed for {handle}: {e}")
        return None


def lookup_channel_by_username(
    youtube: Any,
    username: str
) -> Optional[Dict[str, Any]]:
    """
    Look up channel by legacy username.

    Args:
        youtube: Authenticated YouTube service
        username: Channel username

    Returns:
        Channel data dict or None if not found
    """
    try:
        request = youtube.channels().list(part="id", forUsername=username)
        response = request.execute()
        items = response.get("items", [])
        return items[0] if items else None
    except Exception as e:
        logger.debug(f"forUsername lookup failed for {username}: {e}")
        return None


def clean_handle(handle: str) -> str:
    """
    Remove @ symbol from handle.

    Args:
        handle: Channel handle with or without @

    Returns:
        Clean handle without @
    """
    return handle.lstrip('@')


def find_channel(youtube: Any, handle: str) -> Optional[Channel]:
    """
    Find channel by handle using multiple lookup strategies.

    Args:
        youtube: Authenticated YouTube service
        handle: Channel handle (with or without @)

    Returns:
        Channel object or None if not found
    """
    cleaned = clean_handle(handle)

    # Try lookup strategies in order
    lookup_strategies: List[Callable[[Any, str], Optional[Dict[str, Any]]]] = [
        lookup_channel_by_handle,
        lookup_channel_by_username
    ]

    for strategy in lookup_strategies:
        result = strategy(youtube, cleaned)
        if result:
            return Channel(id=result["id"], handle=handle)

    logger.warning(f"Channel not found: {handle}")
    return None


# Video fetching functions
def fetch_video_page(
    youtube: Any,
    channel_id: str,
    page_token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch a single page of videos from a channel.

    Args:
        youtube: Authenticated YouTube service
        channel_id: Channel ID
        page_token: Pagination token

    Returns:
        API response dict with videos and next page token
    """
    request = youtube.search().list(
        part="id",
        channelId=channel_id,
        maxResults=50,
        pageToken=page_token,
        type="video"
    )
    return request.execute()


def extract_video_ids(response: Dict[str, Any]) -> List[str]:
    """
    Extract video IDs from API response.

    Args:
        response: API response dict

    Returns:
        List of video IDs
    """
    return [item["id"]["videoId"] for item in response.get("items", [])]


def fetch_all_video_ids(youtube: Any, channel_id: str) -> List[str]:
    """
    Fetch all video IDs from a channel using pagination.

    Args:
        youtube: Authenticated YouTube service
        channel_id: Channel ID

    Returns:
        List of all video IDs
    """
    def accumulate_videos(
        acc: tuple[List[str], Optional[str]],
        _: int
    ) -> tuple[List[str], Optional[str]]:
        """Accumulator function for pagination."""
        video_ids, page_token = acc

        if page_token is None and video_ids:  # Already finished
            return acc

        response = fetch_video_page(youtube, channel_id, page_token)
        new_ids = extract_video_ids(response)
        next_token = response.get("nextPageToken")

        return (video_ids + new_ids, next_token)

    # Use reduce to handle pagination functionally
    # Max 100 pages to prevent infinite loops
    final_ids, _ = reduce(
        accumulate_videos,
        range(100),
        ([], None)
    )

    return final_ids


def fetch_channel_videos(youtube: Any, channel_id: str) -> List[Video]:
    """
    Fetch all videos from a channel as Video objects.

    Args:
        youtube: Authenticated YouTube service
        channel_id: Channel ID

    Returns:
        List of Video objects
    """
    video_ids = fetch_all_video_ids(youtube, channel_id)
    return [Video(id=vid_id) for vid_id in video_ids]


# Like functions
def is_quota_exceeded_error(error: googleapiclient.errors.HttpError) -> bool:
    """
    Check if an error is a quota exceeded error.

    Args:
        error: HTTP error from YouTube API

    Returns:
        True if quota exceeded, False otherwise
    """
    error_str = str(error)
    return "quotaExceeded" in error_str or "quota" in error_str.lower()


def like_video(youtube: Any, video: Video) -> LikeResult:
    """
    Like a single video.

    Args:
        youtube: Authenticated YouTube service
        video: Video object

    Returns:
        LikeResult indicating success or failure
    """
    try:
        youtube.videos().rate(id=video.id, rating="like").execute()
        logger.info(f"Liked video: {video.id}")
        return LikeResult(video_id=video.id, success=True)
    except googleapiclient.errors.HttpError as error:
        quota_exceeded = is_quota_exceeded_error(error)
        if quota_exceeded:
            logger.warning(f"⚠️ Quota exceeded while liking video {video.id}")
        else:
            logger.error(f"Failed to like video {video.id}: {error}")
        return LikeResult(
            video_id=video.id,
            success=False,
            error=str(error),
            quota_exceeded=quota_exceeded
        )


def like_videos(youtube: Any, videos: List[Video]) -> List[LikeResult]:
    """
    Like multiple videos.

    Args:
        youtube: Authenticated YouTube service
        videos: List of Video objects

    Returns:
        List of LikeResult objects
    """
    return [like_video(youtube, video) for video in videos]


def like_videos_with_callback(
    youtube: Any,
    videos: List[Video],
    on_progress: Callable[[int, int, Video], None]
) -> List[LikeResult]:
    """
    Like multiple videos with progress callback.
    Stops gracefully when quota is exceeded.

    Args:
        youtube: Authenticated YouTube service
        videos: List of Video objects
        on_progress: Callback function(current, total, video)

    Returns:
        List of LikeResult objects
    """
    results = []
    total = len(videos)

    for i, video in enumerate(videos, 1):
        result = like_video(youtube, video)
        results.append(result)
        on_progress(i, total, video)

        # Stop immediately if quota exceeded
        if result.quota_exceeded:
            logger.warning(
                f"⚠️ YouTube API quota exceeded after {i}/{total} videos. "
                f"Successfully liked {sum(1 for r in results if r.success)} videos. "
                f"Quota resets daily at midnight Pacific Time."
            )
            break

    return results


# High-level workflow functions
def like_all_channel_videos(
    youtube: Any,
    handle: str,
    on_progress: Optional[Callable[[int, int, Video], None]] = None
) -> tuple[Optional[Channel], List[Video], List[LikeResult]]:
    """
    Complete workflow: Find channel, fetch videos, like all videos.

    Args:
        youtube: Authenticated YouTube service
        handle: Channel handle
        on_progress: Optional progress callback

    Returns:
        Tuple of (channel, videos, like_results)
    """
    # Find channel
    channel = find_channel(youtube, handle)
    if not channel:
        return (None, [], [])

    # Fetch videos
    videos = fetch_channel_videos(youtube, channel.id)
    logger.info(f"Found {len(videos)} videos in channel {channel.handle}")

    # Like videos
    if on_progress:
        results = like_videos_with_callback(youtube, videos, on_progress)
    else:
        results = like_videos(youtube, videos)

    # Log summary
    successful = sum(1 for r in results if r.success)
    logger.info(f"Liked {successful}/{len(videos)} videos successfully")

    return (channel, videos, results)
