"""Flask web application for HampterLiker with functional architecture."""

from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import logging

from flask import Flask, render_template, request, jsonify

from config import YouTubeConfig, AppConfig
from youtube_service import (
    get_authenticated_service,
    like_all_channel_videos,
    Video
)


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProcessStatus(Enum):
    """Enumeration of process statuses."""

    IDLE = "idle"
    AUTHENTICATING = "authenticating"
    FETCHING = "fetching"
    LIKING = "liking"
    COMPLETED = "completed"
    ERROR = "error"


@dataclass
class ProgressState:
    """Immutable progress state snapshot."""

    status: ProcessStatus
    message: str
    total_videos: int
    liked_videos: int
    current_video_id: str
    channel_id: str
    channel_name: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            **asdict(self),
            'status': self.status.value
        }

    @classmethod
    def initial(cls) -> 'ProgressState':
        """Create initial idle state."""
        return cls(
            status=ProcessStatus.IDLE,
            message="Ready to start",
            total_videos=0,
            liked_videos=0,
            current_video_id="",
            channel_id="",
            channel_name=""
        )

    def with_status(self, status: ProcessStatus, message: str) -> 'ProgressState':
        """Create new state with updated status and message."""
        return ProgressState(
            status=status,
            message=message,
            total_videos=self.total_videos,
            liked_videos=self.liked_videos,
            current_video_id=self.current_video_id,
            channel_id=self.channel_id,
            channel_name=self.channel_name
        )

    def with_channel(self, channel_id: str, channel_name: str) -> 'ProgressState':
        """Create new state with channel information."""
        return ProgressState(
            status=self.status,
            message=self.message,
            total_videos=self.total_videos,
            liked_videos=self.liked_videos,
            current_video_id=self.current_video_id,
            channel_id=channel_id,
            channel_name=channel_name
        )

    def with_videos(self, total: int) -> 'ProgressState':
        """Create new state with video count."""
        return ProgressState(
            status=self.status,
            message=self.message,
            total_videos=total,
            liked_videos=self.liked_videos,
            current_video_id=self.current_video_id,
            channel_id=self.channel_id,
            channel_name=self.channel_name
        )

    def with_progress(self, liked: int, video_id: str) -> 'ProgressState':
        """Create new state with like progress."""
        return ProgressState(
            status=self.status,
            message=self.message,
            total_videos=self.total_videos,
            liked_videos=liked,
            current_video_id=video_id,
            channel_id=self.channel_id,
            channel_name=self.channel_name
        )


class ProgressManager:
    """Thread-safe progress state manager."""

    def __init__(self):
        """Initialize with idle state."""
        self._state = ProgressState.initial()
        self._lock = threading.Lock()

    def get_state(self) -> ProgressState:
        """Get current state snapshot."""
        with self._lock:
            return self._state

    def update_state(self, new_state: ProgressState) -> None:
        """Update to new state."""
        with self._lock:
            self._state = new_state

    def reset(self) -> None:
        """Reset to initial state."""
        with self._lock:
            self._state = ProgressState.initial()


# Global progress manager
progress_manager = ProgressManager()


def create_app(config: AppConfig) -> Flask:
    """
    Create and configure Flask application.

    Args:
        config: Application configuration

    Returns:
        Configured Flask app
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hampter-loves-you'

    @app.route('/')
    def index() -> str:
        """Render main page."""
        return render_template('index.html')

    @app.route('/start', methods=['POST'])
    def start_liking() -> Dict[str, Any]:
        """Start the liking process."""
        data = request.json or {}
        channel_username = data.get('channel_username', '@the_hampter')

        # Reset progress
        progress_manager.reset()

        # Start background task
        thread = threading.Thread(
            target=run_liking_workflow,
            args=(channel_username,)
        )
        thread.daemon = True
        thread.start()

        return jsonify({'success': True, 'message': 'Started liking process'})

    @app.route('/progress')
    def get_progress() -> Dict[str, Any]:
        """Get current progress."""
        state = progress_manager.get_state()
        return jsonify(state.to_dict())

    return app


def run_liking_workflow(channel_username: str) -> None:
    """
    Run the complete liking workflow in background.

    Args:
        channel_username: YouTube channel handle
    """
    youtube_config = YouTubeConfig.default()

    try:
        # Authentication
        state = progress_manager.get_state()
        progress_manager.update_state(
            state.with_status(
                ProcessStatus.AUTHENTICATING,
                "Authenticating with YouTube..."
            ).with_channel("", channel_username)
        )

        youtube = get_authenticated_service(youtube_config)

        # Fetching
        state = progress_manager.get_state()
        progress_manager.update_state(
            state.with_status(
                ProcessStatus.FETCHING,
                f"Finding channel: {channel_username}"
            )
        )

        # Define progress callback
        def on_progress(current: int, total: int, video: Video) -> None:
            """Handle progress updates."""
            state = progress_manager.get_state()
            new_state = state.with_progress(current, video.id)
            new_state = ProgressState(
                status=ProcessStatus.LIKING,
                message=f"Liked video {current} of {total}",
                total_videos=new_state.total_videos,
                liked_videos=current,
                current_video_id=video.id,
                channel_id=new_state.channel_id,
                channel_name=new_state.channel_name
            )
            progress_manager.update_state(new_state)

        # Execute workflow
        channel, videos, results = like_all_channel_videos(
            youtube,
            channel_username,
            on_progress
        )

        if not channel:
            state = progress_manager.get_state()
            progress_manager.update_state(
                state.with_status(
                    ProcessStatus.ERROR,
                    f"Channel not found: {channel_username}"
                )
            )
            return

        # Update with channel info
        state = progress_manager.get_state()
        progress_manager.update_state(
            state.with_channel(channel.id, channel.handle)
                 .with_videos(len(videos))
        )

        # Completion
        successful = sum(1 for r in results if r.success)
        state = progress_manager.get_state()
        progress_manager.update_state(
            state.with_status(
                ProcessStatus.COMPLETED,
                f"Successfully liked {successful}/{len(videos)} videos! 🐹"
            )
        )

    except Exception as e:
        logger.exception("Error in liking workflow")
        state = progress_manager.get_state()
        progress_manager.update_state(
            state.with_status(
                ProcessStatus.ERROR,
                f"Error: {str(e)}"
            )
        )


def main() -> None:
    """Main entry point."""
    app_config = AppConfig.default()
    app = create_app(app_config)

    logger.info("🐹 Starting HampterLiker Web UI...")
    logger.info(f"📱 Open your browser to: http://{app_config.host}:{app_config.port}")

    app.run(
        host=app_config.host,
        port=app_config.port,
        debug=app_config.debug
    )


if __name__ == '__main__':
    main()
