from dataclasses import dataclass
from passlib.hash import bcrypt

from typing import ClassVar, Dict, List, Optional, Tuple

from backend import db
from .messages import Message


@dataclass
class User:
    id: int
    name: str
    email: str
    password: str
    __tablename__: ClassVar[str] = "Users"
    __columns__: ClassVar[Tuple] = ("id", "name", "email", "password")

    @classmethod
    def find_by_id(cls, id: int) -> Optional["User"]:
        """Get user by id"""

        user = db.filter_by(cls.__tablename__, {"id": id}).fetchone()
        if user is None:
            return None

        return cls(**dict(zip(cls.__columns__, user)))

    def get_messages(self, params: Dict = None) -> List:
        """Return all messages related to the user"""
        if params is None:
            params = {}
        return Message.filter_by({**params, "recipient": self.id})

    @staticmethod
    def generate_passw(passw: str) -> str:
        return bcrypt.hash(passw)

    @staticmethod
    def verify_passw(passw: str, hashed: str) -> bool:
        return bcrypt.verify(passw, hashed)
