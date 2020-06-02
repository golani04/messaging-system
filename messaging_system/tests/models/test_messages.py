import pytest
from backend.models.messages import Message


def test_msg(app):
    msg = Message(1, "Test", "Test...")

    assert msg.id == 1
    assert msg.created_at is not None
    assert msg.is_read is False


@pytest.mark.parametrize("params", [None, {"user_id": 1}, {"user_id": 1, "is_read": False}])
def test_filter_by_user_id(params, app):
    assert Message.filter_by(params) is not None


def test_message_create(app):
    assert Message.create({"subject": "Test", "body": "Testing..."}) is not None


def test_message_find_by_id(app):
    msg = Message.find_by_id(1)
    assert msg is not None


def test_message_delete(app):
    msg = Message.find_by_id(1)
    assert msg is not None
    assert msg.delete() is not None
