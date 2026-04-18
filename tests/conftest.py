"""
conftest.py
-----------
Shared pytest fixtures used by both the public and private test suites.
"""

import pytest
from datetime import date, datetime, timedelta

from streaming.platform import StreamingPlatform
from streaming.artists import Artist
from streaming.albums import Album
from streaming.tracks import (
    AlbumTrack,
    SingleRelease,
    InterviewEpisode,
    NarrativeEpisode,
    AudiobookTrack,
)
from streaming.users import FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.playlists import Playlist, CollaborativePlaylist


# ---------------------------------------------------------------------------
# Helper - timestamps relative to the real current time so that the
# "last 30 days" window in Q2 always contains RECENT sessions.
# ---------------------------------------------------------------------------
FIXED_NOW = datetime.now().replace(microsecond=0)
RECENT = FIXED_NOW - timedelta(days=10)  # well within 30-day window
OLD = FIXED_NOW - timedelta(days=60)  # outside 30-day window


@pytest.fixture
def platform() -> StreamingPlatform:
    """Return a fully populated StreamingPlatform instance."""
    platform = StreamingPlatform("TestStream")

    # ------------------------------------------------------------------
    # Artists
    # ------------------------------------------------------------------
    pixels = Artist("a1", "Pixels", genre="pop")
    drake = Artist("a2", "Drake", genre="hiphop")
    weeknd = Artist("a3", "Weeknd", genre="r&b")
    selena = Artist("a4", "Selena", genre="pop")
    for artist in (pixels, drake, weeknd, selena):
        platform.add_artist(artist)

    # ------------------------------------------------------------------
    # Albums & AlbumTracks
    # ------------------------------------------------------------------
    dd = Album("alb1", "Digital Dreams", artist=pixels, release_year=2022)
    t1 = AlbumTrack("t1", "Pixel Rain", 180, "pop", pixels, track_number=1)
    t2 = AlbumTrack("t2", "Grid Horizon", 210, "pop", pixels, track_number=2)
    t3 = AlbumTrack("t3", "Vector Fields", 195, "pop", pixels, track_number=3)
    for track in (t1, t2, t3):
        dd.add_track(track)
        platform.add_track(track)
        pixels.add_track(track)
    platform.add_album(dd)

    album2 = Album("alb2", "After Hours", artist=weeknd, release_year=2020)

    t4 = AlbumTrack("t4", "Heartless", 355, "r&b", weeknd, track_number=1)
    t5 = AlbumTrack("t5", "City Glow", 205, "r&b", weeknd, track_number=2)

    for track in (t4, t5):
        album2.add_track(track)
        platform.add_track(track)
        weeknd.add_track(track)

    platform.add_album(album2)

    # ------------------------------------------------------------------
    # Single Releases
    # ------------------------------------------------------------------
    t6 = SingleRelease(
        "t6", "God's Plan", 198, "hiphop", drake, release_date=date(2018, 1, 19)
    )
    t7 = SingleRelease(
        "t7", "Calm Down", 210, "pop", selena, release_date=date(2023, 8, 25)
    )

    for track, artist in ((t6, drake), (t7, selena)):
        platform.add_track(track)
        artist.add_track(track)

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    alice = FreeUser("u1", "Alice", age=30)
    bob = PremiumUser("u2", "Bob", age=25, subscription_start=date(2023, 1, 2))
    chad = PremiumUser("u3", "Chad", age=25, subscription_start=date(2024, 3, 1))

    mom = FamilyAccountUser("u3", "Melissa", age=40)
    child = FamilyMember("u4", "Toni", age=16, parent=mom)

    mom.add_sub_user(child)

    for user in (alice, bob, mom, child, chad):
        platform.add_user(user)

    # ------------------------------------------------------------------
    # Listening Sessions
    # ------------------------------------------------------------------

    s1 = ListeningSession("s1", alice, t1, RECENT, 150)
    s2 = ListeningSession("s2", alice, t3, OLD, 185)

    s3 = ListeningSession("s3", bob, t1, RECENT + timedelta(hours=1), 122)
    s4 = ListeningSession("s4", bob, t2, RECENT + timedelta(hours=2), 210)

    for session in (s1, s2, s3, s4):
        platform.record_session(session)

    # ------------------------------------------------------------------
    # Playlists
    # ------------------------------------------------------------------
    p1 = Playlist("p1", "My Playlist Mix", alice)
    p1.add_track(t1)
    p1.add_track(t4)

    p2 = CollaborativePlaylist("p2", "Collab Playlist", bob)
    p2.add_contributor(child)
    p2.add_contributor(mom)
    p2.add_track(t1)
    p2.add_track(t4)
    p2.add_track(t5)
    p2.add_track(t6)
    p2.add_track(t7)

    platform.add_playlist(p1)
    platform.add_playlist(p2)

    return platform


@pytest.fixture
def fixed_now() -> datetime:
    """Expose the shared FIXED_NOW constant to tests."""
    return FIXED_NOW


@pytest.fixture
def recent_ts() -> datetime:
    return RECENT


@pytest.fixture
def old_ts() -> datetime:
    return OLD
