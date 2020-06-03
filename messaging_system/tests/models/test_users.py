from backend.models.messages import Message
from backend.models.users import User


def test_user():
    user = User(1, "Leon", "test@test.com", "password")
    assert user is not None
    assert user.name == "Leon"
    assert user.password == "password"


def test_get_user_messages(app):
    user = User.find_by_id(1)

    assert user is not None
    messages_data = Message.filter_by({"recipient": user.id})
    assert messages_data is not None
    assert user.get_messages() == messages_data
