from backend import db


def test_db_connect(app):
    assert db.conn is not None
