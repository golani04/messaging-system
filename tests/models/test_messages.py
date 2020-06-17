import pytest

from backend import db
from backend.models import validate
from backend.models.mapper import recipients
from backend.models.messages import Message
from backend.models.users import User


_MESSAGES_IDS = {1, 2, 3, 4, 5}
_SOME_USER = 2
_SOME_MESSAGE_ID = 4
_SOME_RECIPIENT = 1
_MESSAGES_IDS_OF_SOME_RECIPIENT = {2, 5}
_READ_MESSAGES_IDS_OF_SOME_RECIPIENT = {5}

_NON_EXISTING_ID = 100_000_001


@pytest.mark.parametrize(
    "params, expected",
    [
        (None, _MESSAGES_IDS),
        ({"recipient": _SOME_RECIPIENT}, _MESSAGES_IDS_OF_SOME_RECIPIENT),
        ({"recipient": _SOME_RECIPIENT, "is_read": False}, _READ_MESSAGES_IDS_OF_SOME_RECIPIENT),
    ],
)
def test_message_filter_by(params, expected, app):
    result = Message.filter_by(params)
    assert result is not None

    messages_id = {message.id for message in result}
    assert messages_id == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        # IF KEY is not exist in a table will be ignored, and
        # because an autorize user search this table, incorrect key can be ignored
        ({"non-existing-key": _NON_EXISTING_ID}, _MESSAGES_IDS),
        ({"recipient": _NON_EXISTING_ID}, []),
    ],
)
def test_message_filter_by_fails(params, expected, app):
    result = Message.filter_by(params)
    assert {message.id for message in result} == set(expected)


def test_message_create(app):
    message = Message(**{"subject": "Test", "body": "Testing...", "owner": _SOME_USER})
    message.create()
    message.save()

    assert message.id == 6


def test_message_create_fails(app):
    message = Message(**{"subject": "Test", "body": "Testing...", "owner": _NON_EXISTING_ID})

    with pytest.raises(validate.ValidationError):
        message.create()
        message.save()


def test_message_find_by_id(app):
    assert Message.find_by_id(_SOME_MESSAGE_ID)


def test_message_find_by_id_fails(app):
    assert Message.find_by_id(_NON_EXISTING_ID) is None


def test_message_delete(app):
    assert Message.find_by_id(_SOME_MESSAGE_ID).delete()
    assert Message.find_by_id(_SOME_MESSAGE_ID) is None


def test_message_delete_owner_and_recipient_is_not(app):
    # let's check that message is exists in mapper table
    ref = db.session.query(recipients).filter_by(m_id=_SOME_MESSAGE_ID).first()
    recipient = ref.r_id
    assert ref.m_id == _SOME_MESSAGE_ID

    msg = Message.find_by_id(_SOME_MESSAGE_ID)
    msg.delete()

    # check if deleted message also was removed from mapper table
    assert db.session.query(recipients).filter_by(m_id=_SOME_MESSAGE_ID).first() is None

    result = User.query.filter(User.id.in_([recipient, msg.owner])).all()
    # user was not affected by deleting his message
    assert [user.id for user in result] == sorted([msg.owner, recipient])
