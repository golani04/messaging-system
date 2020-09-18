from typing import Dict, List

from backend.models.users import User

_SOME_USER_ID = 1
_SOME_USER_EMAIL = "janedoe@test.com"
_SENT_MESSAGES_IDS_BY_SOME_USER = {1}
_RECEIVED_MESSAGES_IDS_BY_SOME_USER = {2, 5}
_SOME_USER_PASSWORD = "password"

_UPDATED_NAME = "Updated name"
_DEFAULT_USERS_COUNT = 3
_SOME_NON_EXISTING_EMAIL = "nonexiting@test.com"


def test_some_user_exists(app):
    assert User.find_by_id(_SOME_USER_ID) is not None


def test_some_user_password(app):
    user = User.find_by_id(_SOME_USER_ID)

    assert user.password != _SOME_USER_PASSWORD
    # same string if generate again shows different hash
    assert user.password != user.generate_passw(_SOME_USER_PASSWORD)

    # check that some_password and hash that stored are actually the same
    assert user.verify_passw(_SOME_USER_PASSWORD, user.password)


def test_get_user_messages(app):
    user = User.find_by_id(_SOME_USER_ID)
    all_messages: Dict[str, List] = user.get_messages()

    received_message_ids = {message.id for message in all_messages["received"]}
    sent_message_ids = {message.id for message in all_messages["sent"]}

    assert received_message_ids == _RECEIVED_MESSAGES_IDS_BY_SOME_USER
    assert sent_message_ids == _SENT_MESSAGES_IDS_BY_SOME_USER


def test_user_authentication(app):
    user = User.autenticate(_SOME_USER_EMAIL)

    assert user is not None
    assert user.id == _SOME_USER_ID
    assert user.email == _SOME_USER_EMAIL


def test_user_autentication_fails(app):
    user = User.autenticate(_SOME_NON_EXISTING_EMAIL)

    assert user is None


def test_user_create(app):
    user = User.create("Tester", "tester@test.com", _SOME_USER_PASSWORD)
    assert user.verify_passw(_SOME_USER_PASSWORD, user.password)

    user.save()
    assert user.id == _DEFAULT_USERS_COUNT + 1


def test_user_update(app):
    user = User.find_by_id(_SOME_USER_ID)
    assert user.name != _UPDATED_NAME

    user.update({"name": _UPDATED_NAME})
    user.save()

    user = User.find_by_id(_SOME_USER_ID)
    assert user.name == _UPDATED_NAME


def test_user_delete(app):
    user = User.find_by_id(_SOME_USER_ID)
    assert user.delete()
