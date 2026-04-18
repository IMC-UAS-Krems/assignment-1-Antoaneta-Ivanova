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
    beyonce = Artist("a5", "Beyonce", genre="pop")
    justin = Artist("a6", "Justin Bieber", genre="pop")

    for artist in (pixels, drake, weeknd, selena, beyonce, justin):
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

    after_hours = Album("alb2", "After Hours", artist=weeknd, release_year=2020)

    t4 = AlbumTrack("t4", "Heartless", 355, "r&b", weeknd, track_number=1)
    t5 = AlbumTrack("t5", "Faith", 283, "r&b", weeknd, track_number=2)
    t6 = AlbumTrack("t6", "Save Your Tears", 216, "r&b", weeknd, track_number=3)

    for track in (t4, t5, t6):
        after_hours.add_track(track)
        platform.add_track(track)
        weeknd.add_track(track)

    platform.add_album(after_hours)

    # ------------------------------------------------------------------
    # Users
    # ------------------------------------------------------------------
    alice = FreeUser("u1", "Alice", age=30)
    jasmine = FreeUser("u2", "Jasmine", age=20)
    jack = FreeUser("u3", "Jack", age=25)

    bob = PremiumUser("u4", "Bob", age=25, subscription_start=date(2023, 1, 1))
    john = PremiumUser("u5", "John", age=18, subscription_start=date(2024, 5, 8))
    betty = PremiumUser("u6", "Betty", age=66, subscription_start=date(2025, 7, 2))

    carl = FamilyAccountUser("u7", "Carl", age=31)
    child1 = FamilyMember("u8", "James", age=21, parent=carl)
    carl.add_sub_user(child1)

    sam = FamilyAccountUser("u9", "Sam", age=21)
    sibling1 = FamilyMember("u10", "Sally", age=20, parent=sam)
    sibling2 = FamilyMember("u11", "Tyla", age=16, parent=sam)
    sam.add_sub_user(sibling1)
    sam.add_sub_user(sibling2)

    for user in (
        alice,
        bob,
        jasmine,
        jack,
        john,
        betty,
        child1,
        sibling1,
        sibling2,
        carl,
        sam,
    ):
        platform.add_user(user)

    # ------------------------------------------------------------------
    # Listening Sessions
    # ------------------------------------------------------------------

    s1 = ListeningSession("s1", alice, t1, RECENT, 150)
    s2 = ListeningSession("s2", jasmine, t1, RECENT + timedelta(hours=1), 120)
    s3 = ListeningSession("s3", bob, t2, RECENT + timedelta(hours=2), 210)
    s4 = ListeningSession("s4", john, t2, RECENT + timedelta(hours=3), 180)
    s5 = ListeningSession("s5", sibling2, t4, RECENT + timedelta(hours=4), 355)
    s6 = ListeningSession("s6", sibling2, t5, RECENT + timedelta(hours=5), 283)
    s7 = ListeningSession("s7", sibling2, t6, RECENT + timedelta(hours=6), 216)
    s9 = ListeningSession("s9", betty, t3, RECENT + timedelta(hours=7), 200)
    s8 = ListeningSession("s8", jack, t3, OLD, 195)

    for session in (s1, s2, s3, s4, s5, s6, s7, s8, s9):
        platform.record_session(session)

    # ------------------------------------------------------------------
    # Single Releases
    # ------------------------------------------------------------------
    t7 = SingleRelease(
        "t7", "God's Plan", 198, "hiphop", drake, release_date=date(2018, 6, 13)
    )
    t8 = SingleRelease(
        "t8", "Calm Down", 210, "pop", selena, release_date=date(2023, 8, 20)
    )

    for track, artist in ((t7, drake), (t8, selena)):
        platform.add_track(track)
        artist.add_track(track)

    # ------------------------------------------------------------------
    # Playlists
    # ------------------------------------------------------------------

    p1 = Playlist("p1", "Alice's Playlist", alice)

    p1.add_track(t1)
    p1.add_track(t4)
    p1.add_track(t6)

    platform.add_playlist(p1)

    p2 = CollaborativePlaylist("p2", "Collab Playlist", bob)
    p2.add_track(t1)
    p2.add_track(t4)
    p2.add_track(t5)
    p2.add_track(t6)
    p2.add_track(t7)
    p2.add_track(t8)

    p2.add_contributor(jasmine)
    p2.add_contributor(jack)
    p2.add_contributor(betty)
    p2.add_contributor(sam)

    p2.remove_contributor(jack)
    p2.remove_contributor(bob)

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
