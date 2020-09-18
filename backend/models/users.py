from enum import IntEnum
from typing import Dict, List, Optional

from passlib.hash import bcrypt_sha256
from sqlalchemy import Column, Integer, String
from sqlalchemy.exc import SQLAlchemyError

from backend import db
from backend.models.exceptions import DeleteError, SaveError
from backend.models.mapper import recipients
from backend.models.types_decorators import SQLAIntEnum

UserRoles = IntEnum("UserRoles", "admin user")


class User(db.Model):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    email = Column(String(128), unique=True, nullable=False)
    password = Column(String(64), nullable=False)
    role = Column(SQLAIntEnum(UserRoles), index=True, default=UserRoles.user.value)

    messages_sent = db.relationship("Message", back_populates="sender", lazy="dynamic")

    @staticmethod
    def generate_passw(passw: str) -> str:
        # bcrypt has 2 issues 1. it will quit on null byte and had maximum
        # capicity of 72 bytes, passlib solves those issues by hashing password
        # using sha256  algorithm and after bcrypting this hash.
        return bcrypt_sha256.hash(passw)

    @staticmethod
    def verify_passw(passw: str, hashed: str) -> bool:
        return bcrypt_sha256.verify(passw, hashed)

    @classmethod
    def autenticate(cls, email: str) -> Optional["User"]:
        return cls.query.filter_by(email=email).one_or_none()

    @classmethod
    def create(cls, name, email, password: str):
        return cls(
            name=name, password=cls.generate_passw(password), email=email, role=UserRoles.user
        )

    @classmethod
    def find_by_id(cls, u_id: int) -> Optional["User"]:
        """Get user by id"""

        return cls.query.get(u_id)

    @classmethod
    def filter_by(cls, current_user_id: int, search_params: Dict = None):
        if search_params is None:
            search_params = {}

        query_params = [getattr(cls, k) == v for k, v in search_params.items() if hasattr(cls, k)]
        # do not include myself
        query_params.append(cls.id != current_user_id)

        return (
            cls.query.join(recipients, recipients.c.r_id == current_user_id)
            .filter(*query_params)
            .all()
        )

    def get_messages(self, params: Dict = None, message_id: int = None) -> Dict[str, List]:
        """Return all messages related to the user"""
        return {
            "received": self.messages_received,
            "sent": self.messages_sent,
        }

    def update(self, params: Dict):
        for k, v in params.items():
            setattr(self, k, v)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            raise DeleteError({"user": ("Failed to delete a user")})

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise SaveError({"user": ("Failed to create/update a user")})
