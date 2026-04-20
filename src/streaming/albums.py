"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""

from typing import List, Set
from .artists import Artist
from .tracks import AlbumTrack


class Album:
    """Collection of tracks by an artist"""

    def __init__(self, album_id: str, title: str, artist: Artist, release_year: int):
        """
        Initializes an album
        Argumentss:
            album_id:  identifier
            title: album title
            artist: person who created the album
            release_year: year of release
        """
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks: List[AlbumTrack] = []

    def add_track(self, track: AlbumTrack) -> None:
        """
        Adds a track to the album and keep it ordered
        """
        track.album = self
        self.tracks.append(track)
        self.tracks.sort(key=lambda track: track.track_number)

    def track_ids(self) -> Set[str]:
        """
        Return all track IDs in album
        """
        return {track.track_id for track in self.tracks}

    def duration_seconds(self) -> int:
        """
        Calculates total duration of the album
        """
        return sum(track.duration_seconds for track in self.tracks)
