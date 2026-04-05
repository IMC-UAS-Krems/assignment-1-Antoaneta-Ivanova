"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""

from .albums import Album
from .artists import Artist
from .playlists import Playlist, CollaborativePlaylist
from .sessions import ListeningSession
from .users import User, PremiumUser, FamilyAccountUser, FamilyMember, FreeUser
from .tracks import Track, Song
from datetime import datetime
from datetime import timedelta

"""https://www.geeksforgeeks.org/python/python-datetime-timedelta-function/"""


class StreamingPlatform:

    def __init__(self, name: str):
        self.name = name
        self._catalogue: dict[str, Track] = {}
        self._users: dict[str, User] = {}
        self._artists: dict[str, Artist] = {}
        self._albums: dict[str, Album] = {}
        self._playlists: dict[str, Playlist] = {}
        self._sessions: list[ListeningSession] = []

    def add_track(self, track: Track) -> None:
        self._catalogue[track.track_id] = track

    def add_user(self, user: User) -> None:
        self._users[user.user_id] = user

    def add_artist(self, artist: Artist) -> None:
        self._artists[artist.artist_id] = artist

    def add_album(self, album: Album) -> None:
        self._albums[album.album_id] = album

    def add_playlist(self, playlist: Playlist) -> None:
        self._playlists[playlist.playlist_id] = playlist

    def record_session(self, session: ListeningSession) -> None:
        self._sessions.append(session)
        session.user.add_session(session)

    def get_track(self, track_id: str) -> Track | None:
        return self._catalogue.get(track_id)

    def get_user(self, user_id: str) -> User | None:
        return self._users.get(user_id)

    def get_artist(self, artist_id: str) -> Artist | None:
        return self._artists.get(artist_id)

    def get_album(self, album_id: str) -> Album | None:
        return self._albums.get(album_id)

    def all_users(self) -> list[User]:
        return list(self._users.values())

    def all_tracks(self) -> list[Track]:
        return list(self._catalogue.values())

    def total_listening_time_minutes(self, start: datetime, end: datetime) -> float:
        total_cumulative_listening_time_in_minutes = 0

        for session in self._sessions:
            if start <= session.timestamp <= end:
                total_cumulative_listening_time_in_minutes += (
                    session.duration_listened_seconds / 60.0
                )

        return total_cumulative_listening_time_in_minutes

    def avg_unique_tracks_per_premium_user(self, days: int = 30) -> float:

        premium_users = []
        for user in self._users.values():
            if isinstance(user, PremiumUser):
                premium_users.append(user)
        if not premium_users:
            return 0.0

        time_window = datetime.now() - timedelta(days=days)
        number_of_unique_tracks = 0

        for premium_user in premium_users:
            unique_tracks = set()
            for session in premium_user.sessions:
                if session.timestamp >= time_window:
                    unique_tracks.add(session.track.track_id)

            number_of_unique_tracks += len(unique_tracks)

        return number_of_unique_tracks / len(premium_users)

    def track_with_most_distinct_listeners(self) -> Track | None:

        if not self._sessions:
            return None

        track_and_users = {}

        for session in self._sessions:
            track = session.track
            user_id = session.user.user_id

            if track not in track_and_users:
                track_and_users[track] = set()

            track_and_users[track].add(user_id)

        highest_count = 0
        track_with_most_distinct_listeners = None

        for track, users in track_and_users.items():
            if len(users) > highest_count:
                highest_count = len(users)
                track_with_most_distinct_listeners = track

        return track_with_most_distinct_listeners

    def avg_session_duration_by_user_type(self) -> list[tuple[str, float]]:

        durations_by_type = {
            "FreeUser": [],
            "PremiumUser": [],
            "FamilyAccountUser": [],
            "FamilyMember": [],
        }

        for session in self._sessions:
            user = session.user
            duration = session.duration_listened_seconds

            if isinstance(user, FreeUser):
                durations_by_type["FreeUser"].append(duration)
            elif isinstance(user, PremiumUser):
                durations_by_type["PremiumUser"].append(duration)
            elif isinstance(user, FamilyAccountUser):
                durations_by_type["FamilyAccountUser"].append(duration)
            elif isinstance(user, FamilyMember):
                durations_by_type["FamilyMember"].append(duration)

        averages = []
        for type_name, durations in durations_by_type.items():
            if durations:
                avg = sum(durations) / len(durations)
                averages.append((type_name, float(avg)))

        averages.sort(key=lambda x: x[1], reverse=True)
        return averages

    def total_listening_time_underage_sub_users_minutes(
        self, age_threshold: int = 18
    ) -> float:

        total_minutes = 0.0

        for session in self._sessions:
            user = session.user

            if isinstance(user, FamilyMember) and user.age < age_threshold:
                total_minutes += session.duration_listened_seconds / 60.0

        return total_minutes

    def top_artists_by_listening_time(self, n: int = 5) -> list[tuple[Artist, float]]:

        artist_minutes = {}

        for listening_session in self._sessions:
            if isinstance(listening_session.track, Song):
                artist = listening_session.track.artist
                minutes = listening_session.duration_listened_minutes()

                if artist not in artist_minutes:
                    artist_minutes[artist] = 0.0

                artist_minutes[artist] += minutes

        top_artists = sorted(
            artist_minutes.items(), key=lambda item: item[1], reverse=True
        )

        return top_artists[:n]

    def user_top_genre(self, user_id: str) -> tuple[str, float] | None:

        user = self._users.get(user_id)
        if not user or not user.sessions:
            return None

        genre_and_time = {}

        for session in user.sessions:
            genre = session.track.genre
            duration = session.duration_listened_seconds

            genre_and_time[genre] = genre_and_time.get(genre, 0) + duration

        top_genre, top_time = max(genre_and_time.items(), key=lambda x: x[1])

        total_time = sum(genre_and_time.values())

        percentage = (top_time / total_time) * 100

        return (top_genre, percentage)

    def collaborative_playlists_with_many_artists(
        self, threshold: int = 3
    ) -> list[CollaborativePlaylist]:

        result = []

        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                artists_in_playlist = set()

                for track in playlist.tracks:
                    if isinstance(track, Song):
                        artists_in_playlist.add(track.artist)

                if len(artists_in_playlist) > threshold:
                    result.append(playlist)

        return result

    def avg_tracks_per_playlist_type(self) -> dict[str, float]:

        total_tracks_playlist = 0
        count_playlist = 0

        total_tracks_collab = 0
        count_collab = 0

        for playlist in self._playlists.values():
            if isinstance(playlist, CollaborativePlaylist):
                total_tracks_collab += len(playlist.tracks)
                count_collab += 1
            else:
                total_tracks_playlist += len(playlist.tracks)
                count_playlist += 1

        avg_playlist = (
            total_tracks_playlist / count_playlist if count_playlist > 0 else 0.0
        )

        avg_collab = total_tracks_collab / count_collab if count_collab > 0 else 0.0

        return {
            "Playlist": avg_playlist,
            "CollaborativePlaylist": avg_collab,
        }

    def users_who_completed_albums(self) -> list[tuple[User, list[str]]]:
        result = []

        for user in self._users.values():
            user_track_ids = user.unique_tracks_listened()
            completed_albums = []

            for album in self._albums.values():
                if not album.tracks:
                    continue

                album_track_ids = album.track_ids()

                if album_track_ids.issubset(user_track_ids):
                    completed_albums.append(album.title)

            if completed_albums:
                result.append((user, completed_albums))

        return result
