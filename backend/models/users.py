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

    @staticmethod
    def generate_passw(passw: str) -> str:
        return bcrypt.hash(passw)

    @staticmethod
    def verify_passw(passw: str, hashed: str) -> bool:
        return bcrypt.verify(passw, hashed)

    @classmethod
    def find_by_id(cls, id: int) -> Optional["User"]:
        """Get user by id"""

        user = db.filter_by(cls.__tablename__, {"id": id}).fetchone()
        if user is None:
            return None

        return cls(**dict(zip(cls.__columns__, user)))

    @classmethod
    def autenticate(cls, email: str) -> Optional["User"]:
        user = db.filter_by(cls.__tablename__, {"email": email}).fetchone()
        if user is None:
            return None

        return cls(**dict(zip(cls.__columns__, user)))

    def get_messages(self, params: Dict = None, message_id: int = None) -> List:
        """Return all messages related to the user"""
        if params is None:
            params = {}

        params = {**params, "recipient": self.id}
        if message_id is not None:
            params["id"] = message_id
        return Message.filter_by(params)
