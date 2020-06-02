from backend.models.users import User


def test_user():
    user = User(1, "Leon", "test@test.com", "password")
    assert user is not None
    assert user.name == "Leon"
    # TODO: when jwt will be introduced check that password encrypted
    assert user.password == "password"


def test_get_user_messages(app):
    user = User.find_by_id(1)

    assert user is not None
    assert user.messages() is not None
