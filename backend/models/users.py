from passlib.hash import bcrypt

from typing import Dict, List, Optional

from sqlalchemy import Column, Integer, String
from backend import db

from .mapper import recipients


class User(db.Model):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), unique=True, nullable=True)
    email = Column(String(128), unique=True, nullable=True)
    password = Column(String(64), unique=True, nullable=True)

    messages_sent = db.relationship("Message", back_populates="sender")
    messages_recieved = db.relationship(
        "Message", secondary=recipients, primaryjoin=(recipients.c.r_id == id)
    )

    @staticmethod
    def generate_passw(passw: str) -> str:
        return bcrypt.hash(passw)

    @staticmethod
    def verify_passw(passw: str, hashed: str) -> bool:
        return bcrypt.verify(passw, hashed)

    @classmethod
    def find_by_id(cls, u_id: int) -> Optional["User"]:
        """Get user by id"""

        return cls.query.get(u_id)

    @classmethod
    def autenticate(cls, email: str) -> Optional["User"]:
        return cls.query.filter_by(email=email).one_or_none()

    def get_messages(self, params: Dict = None, message_id: int = None) -> Dict[str, List]:
        """Return all messages related to the user"""
        return {
            "recieved": self.messages_recieved,
            "sent": self.messages_sent,
        }
