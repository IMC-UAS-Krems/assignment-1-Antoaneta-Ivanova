"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

from typing import List
from .tracks import Track
from .users import User


class Playlist:
    """A collection of tracks created by a user"""

    def __init__(self, playlist_id: str, name: str, owner: User):
        """
        Initializes a playlist
        Arguments:
            playlist_id: identifier
            name: playlist name
            owner: user who owns the playlist
        """
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks: List[Track] = []

    def add_track(self, track: Track) -> None:
        """Adds a track if it is not in the playlist"""
        if track not in self.tracks:
            self.tracks.append(track)

    def remove_track(self, track_id: str) -> None:
        """Remove a track by its ID"""
        self.tracks = [track for track in self.tracks if track.track_id != track_id]

    def total_duration_seconds(self) -> int:
        """Calculates total duration of all tracks"""
        return sum(track.duration_seconds for track in self.tracks)


class CollaborativePlaylist(Playlist):
    """A playlist that allows multiple users to contribute"""

    def __init__(self, playlist_id: str, name: str, owner: User):
        """Initialize a collaborative playlist"""
        super().__init__(playlist_id, name, owner)
        self.contributors: List[User] = [owner]

    def add_contributor(self, user: User) -> None:
        """Add a contributor to the playlist"""
        if user not in self.contributors:
            self.contributors.append(user)

    def remove_contributor(self, user: User) -> None:
        """Remove a contributor (owner cannot be removed)"""
        if user == self.owner:
            return
        if user in self.contributors:
            self.contributors.remove(user)
