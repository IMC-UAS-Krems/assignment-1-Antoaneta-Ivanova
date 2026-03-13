"""
sessions.py
-----------
Implement the ListeningSession class for recording listening events.

Classes to implement:
  - ListeningSession
"""
from users import User

class ListeningSession:
        
        def __init__(self, session_id: str, user: User, track, timestamp: datetime, duration_listened_seconds: int)
                self.session_id = session_id
                self.user = user
                self.track = track
                self.timestamp  = timestamp
                self.duration_listened_seconds = duration_listened_seconds
        
        def duration_listened_minutes(self) -> float:
                pass
