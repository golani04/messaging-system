from datetime import datetime
from time import time

from typing import Any, Dict, List, Optional, Union

from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey
from sqlalchemy.exc import SQLAlchemyError

from backend import db
from .mapper import recipients
from .validate import ValidationError


class Message(db.Model):
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(128), unique=True, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(Integer, default=lambda: int(time()))
    is_read = Column(Boolean, default=False)
    owner = Column(Integer, ForeignKey("Users.id"), index=True)

    sender = db.relationship("User", back_populates="messages_sent")
    recipients = db.relationship(
        "User",
        secondary=recipients,
        primaryjoin=(recipients.c.m_id == id),
        backref=db.backref("Users"),
    )

    @classmethod
    def filter_by(cls, params: Dict[str, Any] = None) -> List["Message"]:
        """Return messages based on prams, if params is None return all messages."""
        query = cls.query
        if params is None:
            params = {}

        recipient = params.pop("recipient", None)
        query_params = [getattr(cls, k) == v for k, v in params.items() if hasattr(cls, k)]

        if recipient is not None:
            query = query.join(recipients, recipients.c.m_id == cls.id)
            query_params.append(recipients.c.r_id == recipient)

        return query.filter(*query_params).all()

    @classmethod
    def find_by_id(cls, m_id: str) -> Optional["Message"]:
        """Use filter_by to find message."""
        # TODO: figure out how to add that message is read by recipient

        return cls.query.get(m_id)

    def create(self) -> Union["Message", str]:
        """Create a new message using db class"""
        self.created_at = int(time())
        self.is_read = False

    def delete(self) -> int:
        """Delete function shoud invoke delete"""
        try:
            db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            db.session.rollback()
            raise ValidationError

    def to_json(self):
        # TODO: iclude owner as User object and not only an id

        return {
            "id": self.id,
            "subject": self.subject,
            "body": self.body,
            "owner": self.owner,
            "created_at": datetime.utcfromtimestamp(self.created_at),
            "is_read": self.is_read,
        }

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise ValidationError
