"""
artists.py
----------
Implement the Artist class representing musicians and content creators.

Classes to implement:
  - Artist
"""

from .tracks import Track
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from .tracks import Track


class Artist:
    """a creator on the platform"""

    def __init__(self, artist_id: str, name: str, genre: str):
        """
        Initialize an artist.
        Arguments:
            artist_id: identifier
            name: artist name
            genre: style of genre
        """
        self.artist_id = artist_id
        self.name = name
        self.genre = genre
        self.tracks: List["Track"] = []

    def add_track(self, track: "Track") -> None:
        """Adds a track to the artist if not there"""
        if track not in self.tracks:
            self.tracks.append(track)

    def track_count(self) -> int:
        """Returns number of tracks by this artist"""
        return len(self.tracks)
