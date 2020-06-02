from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    id: int
    name: str
    email: str
    # TODO: password should be bcrypted
    password: str

    def find_by_id(cls, id: int) -> Optional["User"]:
        """Get user by id"""

    def messages(self) -> List:
        """Return all messages related to the user"""
