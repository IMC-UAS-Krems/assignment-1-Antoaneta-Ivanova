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
    def __init__(self, album_id: str, title: str, artist: Artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks: List[AlbumTrack] = []

    def add_track(self, track: AlbumTrack) -> None:
        if track not in self.tracks:
            self.tracks.append(track)
            track.album = self  # This is added cause track belongs to the album, and an album consists of albumtrack, aka. bidirectional association

    def track_ids(self) -> Set[str]:
        return {track.track_id for track in self.tracks}

    def duration_seconds(self) -> int:
        return sum(track.duration_seconds for track in self.tracks)
