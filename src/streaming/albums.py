"""
albums.py
---------
Implement the Album class for collections of AlbumTrack objects.

Classes to implement:
  - Album
"""

from .artists import Artist


class Album:
    def __init__(self, album_id: str, title: str, artist: Artist, release_year: int):
        self.album_id = album_id
        self.title = title
        self.artist = artist
        self.release_year = release_year
        self.tracks = []

    def add_track(self, track) -> None:
        pass

    def track_ids(self):
        pass

    def duration_seconds(self):
        pass
