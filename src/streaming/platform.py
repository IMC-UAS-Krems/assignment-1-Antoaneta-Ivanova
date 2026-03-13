"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

from albums import Artist
from artists import Album
from playlists import Playlist
from sessions import ListeningSession
from users import User


class StreamingPlatform:

    def __init__(self, name: str):
        self.name = name
        self._catalogue = {}
        self._users = {}
        self._artists = {}
        self._albums = {}
        self._playlists = {}
        self._sessions = {}

    def add_track(self, track) -> None:
        pass

    def add_user(self, user) -> None:
        pass

    def add_artist(self, artist) -> None:
        pass

    def add_album(self, album) -> None:
        pass

    def add_playlist(self, playlist) -> None:
        pass

    def record_session(self, session) -> None:
        pass

    def get_track(self, track_id=None):
        pass

    def get_user(self, user_id=None):
        pass

    def get_artist(self, artist_id=None):
        pass

    def get_album(self, album_id=None):
        pass

    def all_users(self, album) -> list[User]:
        pass

    def all_tracks(self, album) -> list[Track]:
        pass
