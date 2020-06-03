from dataclasses import asdict, dataclass, field
from datetime import datetime
from time import time

from typing import Any, ClassVar, Dict, Optional, Union

from backend import db
from . import validate


@dataclass
class Message:
    subject: str
    body: str
    owner: int
    created_at: int = field(default=None, metadata="If `None` means is not saved")
    id: int = field(default=0, metadata="If `0` means is not saved")
    is_read: bool = False
    __tablename__: ClassVar[str] = "Messages"
    __columns__: ClassVar[tuple] = ("id", "subject", "body", "created_at", "is_read", "owner")

    def __post_init__(self):
        self._validate(asdict(self))
        self.created_at = self.convert_to_timestamp(self.created_at)

    @staticmethod
    def convert_to_timestamp(dt):
        if dt is None:
            return None

        if isinstance(dt, str):
            dt = datetime.fromisoformat(dt)

        return int(datetime.timestamp(dt)) if isinstance(dt, datetime) else dt

    @staticmethod
    def _validate(data: Dict):
        required_fields = {"subject", "body", "owner"}
        validate.required_fields(required_fields, set(data))
        validate.is_numeric([v for k, v in data.items() if k in {"id", "owner"}])
        validate.is_datetime(data.get("created_at"))

    @classmethod
    def filter_by(cls, params: Dict[str, Any] = None) -> Optional["Message"]:
        """Return messages based on prams, if params is None return all messages."""

        if params is None:
            return db.filter_by(cls.__tablename__, {}).fetchall()

        return db.filter_by(
            cls.__tablename__, params, "UserMessages", ("r_id", "recipient", "m_id")
        ).fetchall()

    @classmethod
    def find_by_id(cls, id: str) -> Optional["Message"]:
        """Use filter_by to find message."""

        message = db.filter_by(cls.__tablename__, {"id": id}).fetchone()
        if message is None:
            return None
        return cls(**dict(zip(cls.__columns__, message)))

    def create(self) -> Union["Message", str]:
        """Create a new message using db class"""
        data = {**asdict(self), "created_at": int(time()), "is_read": int(False)}

        # remove id
        data.pop("id", None)
        self.id = db.insert(Message.__tablename__, data)

        if self.id > 0:
            self.created_at = data["created_at"]
            self.is_read = data["is_read"]
        else:
            raise validate.ValidationError("Add a new message is failed")

    def delete(self) -> Optional["Message"]:
        """Delete function shoud invoke delete on db global class to remove self instance"""
