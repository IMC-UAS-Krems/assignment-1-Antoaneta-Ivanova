"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""

from .users import User
from .tracks import Track
from datetime import datetime


class ListeningSession:
    """Represents a single listening event of a user playing a track"""

    def __init__(
        self,
        session_id: str,
        user: User,
        track: Track,
        timestamp: datetime,
        duration_listened_seconds: int,
    ):
        """
        Initializes a listening session

        Arguments:
            session_id: identifier
            user: user who listened
            track: track that was played
            timestamp: when the session happened
            duration_listened_seconds: time listened in seconds
        """

        self.session_id = session_id
        self.user = user
        self.track = track
        self.timestamp = timestamp
        self.duration_listened_seconds = duration_listened_seconds

    def duration_listened_minutes(self) -> float:
        """Converts listened duration to minutes"""
        return self.duration_listened_seconds / 60.0
