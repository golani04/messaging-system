from backend.models.users import User


def test_user():
    user = User(1, "Leon", "test@test.com", "password")
    assert user is not None
    assert user.name == "Leon"
    # checking that password is encrepted
    assert user.password != "password"
    assert user.verify_passw("password", user.password)


def test_get_user_messages(app):
    user = User.find_by_id(1)

    assert user is not None
    assert user.messages() is not None
