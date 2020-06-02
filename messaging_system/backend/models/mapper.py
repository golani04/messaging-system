from dataclasses import dataclass
from typing import List

from .messages import Message


@dataclass
class Mapper:
    m_id: int
    s_id: int
    r_id: int

    def get_messages_by_recipient(self, is_read: bool = None) -> List[Message]:
        """Join 2 tables by r_id == Users.id and m_id == Messages.id"""
