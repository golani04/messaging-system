import pytest
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
    assert Message.create({"subject": "Test", "body": "Testing..."}) is not None


def test_message_find_by_id(app):
    msg = Message.find_by_id(1)
    assert msg is not None


def test_message_delete(app):
    msg = Message.find_by_id(1)
    assert msg is not None
    assert msg.delete() is not None
