from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime
from typing import List, Set, Union, Optional


@dataclass
class ValidationError(Exception):
    messages: str


def required_fields(req_fields: Set, keys: Set) -> bool:
    if req_fields <= keys:
        return True

    raise ValidationError(f"Missing required fields: {','.join(req_fields - keys)}")


def is_numeric(nums: Union[int, List[int]]) -> bool:
    if isinstance(nums, int):
        return True
    if isinstance(nums, Iterable):
        if all(isinstance(num, int) for num in nums):
            return True

    raise ValidationError("Provided values are not of type integer")


def is_datetime(dt: Optional[Union[int, str, datetime]]) -> bool:
    if dt is None:
        return None
    if isinstance(dt, datetime):
        return True

    try:
        return bool(
            datetime.fromisoformat(dt) if isinstance(dt, str) else datetime.utcfromtimestamp(dt)
        )
    except (TypeError, ValueError, OSError):
        # OSError - if integer argument is invalid
        raise ValidationError("Datetime is invalid")
