from dataclasses import dataclass, field
from datetime import datetime

from typing import Any, Dict, Optional


@dataclass
class Message:
    id: int
    subject: str
    body: str
    created_at: datetime = field(default=datetime.utcnow)
    is_read: bool = False

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
