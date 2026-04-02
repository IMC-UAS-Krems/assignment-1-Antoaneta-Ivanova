from datetime import date, datetime

from streaming.users import User, FreeUser, PremiumUser, FamilyAccountUser, FamilyMember
from streaming.sessions import ListeningSession
from streaming.tracks import Track
from streaming.artists import Artist
from streaming.tracks import SingleRelease


class TestUsers:
    def test_add_session_appends(self) -> None:
        user = User("u1", "User", age=20)
        track = Track("t1", "Track", 120, "pop")
        session = ListeningSession("s1", user, track, datetime(2024, 1, 1), 120)
        user.add_session(session)
        assert user.sessions == [session]

    def test_total_listening_seconds_empty(self) -> None:
        user = User("u1", "User", age=20)
        assert user.total_listening_seconds() == 0

    def test_total_listening_seconds_sum(self) -> None:
        user = User("u1", "User", age=20)
        track = Track("t1", "Track", 120, "pop")
        s1 = ListeningSession("s1", user, track, datetime(2024, 1, 1), 120)
        s2 = ListeningSession("s2", user, track, datetime(2024, 1, 1), 60)
        user.add_session(s1)
        user.add_session(s2)
        assert user.total_listening_seconds() == 180

    def test_total_listening_minutes(self) -> None:
        user = User("u1", "User", age=20)
        track = Track("t1", "Track", 120, "pop")
        session = ListeningSession("s1", user, track, datetime(2024, 1, 1), 120)
        user.add_session(session)
        assert user.total_listening_minutes() == 2.0

    def test_unique_tracks_listened(self) -> None:
        user = User("u1", "User", age=20)
        t1 = Track("t1", "Track 1", 120, "pop")
        t2 = Track("t2", "Track 2", 120, "pop")
        user.add_session(ListeningSession("s1", user, t1, datetime(2024, 1, 1), 120))
        user.add_session(ListeningSession("s2", user, t2, datetime(2024, 1, 1), 120))
        assert user.unique_tracks_listened() == {"t1", "t2"}

    def test_unique_tracks_listened_dedupes(self) -> None:
        user = User("u1", "User", age=20)
        t1 = Track("t1", "Track 1", 120, "pop")
        user.add_session(ListeningSession("s1", user, t1, datetime(2024, 1, 1), 120))
        user.add_session(ListeningSession("s2", user, t1, datetime(2024, 1, 1), 120))
        assert user.unique_tracks_listened() == {"t1"}

    def test_free_user_is_user(self) -> None:
        user = FreeUser("u1", "User", age=20)
        assert isinstance(user, User)

    def test_premium_user_subscription_start(self) -> None:
        start = date(2023, 1, 1)
        user = PremiumUser("u1", "User", age=20, subscription_start=start)
        assert user.subscription_start == start

    def test_family_account_add_member(self) -> None:
        family = FamilyAccountUser("u1", "Parent", age=40)
        member = FamilyMember("u2", "Child", age=16, parent=family)
        family.add_sub_user(member)
        assert member in family.sub_users

    def test_family_account_all_members(self) -> None:
        family = FamilyAccountUser("u1", "Parent", age=40)
        member = FamilyMember("u2", "Child", age=16, parent=family)
        family.add_sub_user(member)
        assert family.all_members() == [family, member]

    def test_family_member_parent(self) -> None:
        family = FamilyAccountUser("u1", "Parent", age=40)
        member = FamilyMember("u2", "Child", age=16, parent=family)
        assert member.parent is family

    def test_family_account_multiple_members(self) -> None:
        family = FamilyAccountUser("u1", "Parent", age=40)
        member1 = FamilyMember("u2", "Child 1", age=16, parent=family)
        member2 = FamilyMember("u3", "Child 2", age=14, parent=family)
        family.add_sub_user(member1)
        family.add_sub_user(member2)
        assert len(family.sub_users) == 2
