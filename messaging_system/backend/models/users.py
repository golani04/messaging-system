from dataclasses import dataclass
from passlib.hash import bcrypt

from typing import List, Optional


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str

    def __post_init__(self):
        self.password = self.generate_passw(self.password)

    def find_by_id(cls, id: int) -> Optional["User"]:
        """Get user by id"""

    def messages(self) -> List:
        """Return all messages related to the user"""

    @staticmethod
    def generate_passw(passw: str) -> str:
        return bcrypt.hash(passw)

    @staticmethod
    def verify_passw(passw: str, hashed: str) -> bool:
        return bcrypt.verify(passw, hashed)
