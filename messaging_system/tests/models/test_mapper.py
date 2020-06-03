import pytest
from backend import db
from backend.models import mapper, messages, validate


@pytest.mark.parametrize("s_id, r_id", [(1000001, 1), (1, 1000001)])
def test_mapper_create_transaction_fails(s_id, r_id, app):
    message = messages.Message("Test mapper", "Testing...", s_id)

    with pytest.raises(validate.ValidationError):
        # NOTE: using with and if error raised it will call rollback
        with db.conn:
            message.create()
            mapper.create_ref(message, r_id)

    res = db.conn.execute("SELECT * FROM Messages where id = ?", (message.id,)).fetchone()
    assert res is None

    res = db.conn.execute(
        "SELECT * FROM UserMessages where m_id = ? and r_id = ?", (message.id, r_id)
    ).fetchone()
    assert res is None


def test_mapper_create(app):
    # return lastrowid, initial database has 5 rows
    assert mapper.create_ref(messages.Message.find_by_id(1), 3) == 6
