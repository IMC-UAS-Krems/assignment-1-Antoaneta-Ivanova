"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""

from users import User

class Playlist:
    def __init__(self, playlist_id: str, name: str, owner: User):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []
        
    def add_track(self, track) -> None: 
        pass
    
    def remove_track(self, track_id) -> None:
        pass
    
    def total_duration_seconds(self) -> int:
        pass


class CollaborativePlaylist(Playlist):
        
        def __init__(self, playlist_id: str, name: str, owner: User):
             super().__init__(playlist_id, name, owner)
             self.contributors = []
        
        def add_contributor(self, user) -> None: 
             pass
        
        def remove_contributor(self, user) -> None: 
             pass
