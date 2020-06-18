import pytest
from backend import db
from backend.models import users, mapper, messages, exceptions

_SOME_USER_ID = 1
_SOME_MESSAGE_ID_OF_THE_SOME_USER = 3
_DEFAULT_LENGTH_OF_MESSAGE_IDS_CONNECTED_TO_USERS = 5
_NON_EXISTING_USER_ID = 100_000_001


@pytest.mark.parametrize(
    "sender, recipient",
    [(_NON_EXISTING_USER_ID, _SOME_USER_ID), (_SOME_USER_ID, _NON_EXISTING_USER_ID)],
)
def test_message_create_fails_using_join(sender, recipient, app):
    """Test. Once sender is non existing, once recipient non existing."""

    with pytest.raises(exceptions.SaveError):
        message = messages.Message.create(subject="Test mapper", body="Testing...", owner=sender)
        message.recipients.append(users.User.query.get(recipient))
        message.save()

    # If sender or recipient are not valid users, those statements fail
    res = db.engine.execute("SELECT * FROM Messages where id = ?", (message.id,)).fetchone()
    assert res is None

    res = db.engine.execute(
        "SELECT * FROM UserMessages where m_id = ? and r_id = ?", (message.id, recipient)
    ).fetchone()
    assert res is None


def test_mapper_create(app):
    # return lastrowid, initial database has 5 rows
    message = messages.Message.query.get(_SOME_USER_ID)
    message.recipients.append(users.User.query.get(_SOME_MESSAGE_ID_OF_THE_SOME_USER))
    message.save()

    assert (
        db.session.query(mapper.recipients).count()
        == _DEFAULT_LENGTH_OF_MESSAGE_IDS_CONNECTED_TO_USERS + 1
    )
