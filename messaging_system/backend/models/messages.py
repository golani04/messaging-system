from dataclasses import asdict, dataclass, field
from datetime import datetime

from typing import Any, ClassVar, Dict, Optional

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

    def get_all(self):
        """Return all messages"""

    @classmethod
    def create(cls, data) -> "Message":
        """Create a new message using db class"""
        # TODO: sender and recipient can not be the same

    @classmethod
    def filter_by(cls, params: Dict[str, Any] = None) -> Optional["Message"]:
        """Return messages based on prams, if params is None return all messages."""

    @classmethod
    def find_by_id(self, id: str) -> Optional["Message"]:
        """Use filter_by to find message."""

    def delete(self) -> Optional["Message"]:
        """Delete function shoud invoke delete on db global class to remove self instance"""
