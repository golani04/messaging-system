from dataclasses import is_dataclass

import pytest
from backend.models import validate
from backend.models.messages import Message


def test_msg(app):
    msg = Message("Test", "Test...", 1)

    assert msg.id == 0
    assert msg.created_at is None
    assert msg.is_read is False


@pytest.mark.parametrize(
    "params, expected", [(None, 5), ({"recipient": 1}, 2), ({"recipient": 1, "is_read": False}, 1)]
)
def test_message_filter_by(params, expected, app):
    result = Message.filter_by(params)

    assert result is not None
    assert len(result) == expected


def test_message_create(app):
    msg = Message(**{"subject": "Test", "body": "Testing...", "owner": 1})
    msg.create()

    assert is_dataclass(msg)


def test_message_create_fails(app):
    # owner is not exist
    non_exist_owner = 10001
    msg = Message(**{"subject": "Test", "body": "Testing...", "owner": non_exist_owner})

    with pytest.raises(validate.ValidationError) as excinfo:
        msg.create()

    assert is_dataclass(msg)
    assert str(excinfo.value) == "Add a new message is failed"


def test_message_find_by_id(app):
    msg = Message.find_by_id(1)
    assert is_dataclass(msg)


def test_message_find_by_id_fails(app):
    non_exist_msg = 10001

    assert Message.find_by_id(non_exist_msg) is None


def test_message_delete(app):
    msg = Message.find_by_id(1)
    assert msg is not None
    assert msg.delete() is not None
