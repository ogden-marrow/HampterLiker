"""Configuration module for HampterLiker."""

from typing import List
from dataclasses import dataclass


@dataclass(frozen=True)
class YouTubeConfig:
    """Immutable configuration for YouTube API."""

    scopes: List[str]
    api_service_name: str
    api_version: str

    @classmethod
    def default(cls) -> 'YouTubeConfig':
        """Create default YouTube API configuration."""
        return cls(
            scopes=["https://www.googleapis.com/auth/youtube.force-ssl"],
            api_service_name="youtube",
            api_version="v3"
        )


@dataclass(frozen=True)
class AppConfig:
    """Immutable configuration for Flask application."""

    host: str
    port: int
    debug: bool

    @classmethod
    def default(cls) -> 'AppConfig':
        """Create default Flask app configuration."""
        return cls(
            host="localhost",
            port=5000,
            debug=True
        )
