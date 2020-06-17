from time import time

from typing import Any, Dict, List, Optional

from sqlalchemy import Boolean, Column, Integer, String, Text, ForeignKey
from sqlalchemy.exc import SQLAlchemyError

from backend import db
from .exceptions import DeleteError, SaveError, ValidationError
from .mapper import recipients
from .users import User


class Message(db.Model):
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(128), unique=True, nullable=False)
    body = Column(Text, nullable=False)
    created_at = Column(Integer, default=lambda: int(time()), nullable=False)
    is_read = Column(Boolean, default=False)
    # CONSIDER: maybe I don't need this field and can delegate it to the mapper table
    owner = Column(Integer, ForeignKey("Users.id"), nullable=False, index=True)

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
        # TODO: figure out how to add that message is read by recipient

        return cls.query.get(m_id)

    @classmethod
    def create(cls, subject: str, body: str, owner: int) -> "Message":
        return cls(subject=subject, body=body, owner=owner, created_at=int(time()), is_read=False)

    def delete(self, user: User) -> bool:
        try:
            if user in self.recipients:
                self.recipients.remove(user)
            elif self.owner == user.id:
                db.session.delete(self)
            db.session.commit()
            return True
        except SQLAlchemyError:
            # TODO: send email to support team or devops
            db.session.rollback()
            raise DeleteError(
                {
                    "message": (
                        "Deleting a message failed due to the internal error. "
                        "Support team is notified."
                    )
                }
            )
        #
        raise ValidationError(
            {"message": "Message can be deleted only by a recipient or by a sender"}
        )

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            raise SaveError(
                {
                    "message": (
                        "Sending a message failed due to internal error. "
                        "Support team is notified."
                    )
                }
            )
