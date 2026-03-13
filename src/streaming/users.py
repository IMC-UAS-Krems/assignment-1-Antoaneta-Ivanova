"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

import abc


class User(abc.ABC):
    def __init__(self, user_id: str, name: str, age: int):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    @abc.abstractmethod
    def add_session(self, session) -> None:
        pass

    @abc.abstractmethod
    def total_listening_seconds(self) -> int:
        pass

    @abc.abstractmethod
    def total_listening_minutes(self) -> float:
        pass

    @abc.abstractmethod
    def unique_tracks_listened(self) -> set[str]:
        pass


class FreeUser(User):
    MAX_SKIPS_PER_HOUR = 6


class PremiumUser(User):

    def __init__(self, user_id: str, name: str, age: int, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(User): 
    
    def __init__(self, user_id: str, name: str, age: int):
        super().__init__(user_id, name, age)
        self.sub_users= []
    
    def add_sub_user(self, sub_user) -> None: 
        pass
    
    def all_members(self) -> #list[User]
        pass


class FamilyMember(User):

    def __init__(self, user_id: str, name: str, age: int, parent: FamilyAccountUser):
        super().__init__(user_id, name, age)
        self.parent = parent
