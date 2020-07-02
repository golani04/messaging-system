import pytest

from flask_jwt_extended import create_access_token


_SOME_USER_ID = 1
_SOME_USER_MESSAGE_ID_AS_OWNER = 1
_SOME_USER_MESSAGE_ID_AS_RECIPIENT = 2
_SOME_USER_MESSAGES_IDS_AS_RECIPIENT = {2, 5}
_READ_SOME_USER_MESSAGES_IDS_AS_RECIPIENT = {2}
_UNREAD_SOME_USER_MESSAGES_IDS_AS_RECIPIENT = {5}
_SOME_RECIPIENT_ID = 2
_SOME_RECIPIENT_MESSAGES_IDS_AS_RECIPIENT = {1}
_READ_SOME_RECIPIENT_MESSAGES_IDS_AS_RECIPIENT = {1}
_UNREAD_SOME_RECIPIENT_MESSAGES_IDS_AS_RECIPIENT = set()
_DEFAULT_LENGTH_OF_MESSAGES_TABLE = 5
_SOME_NON_EXISTING_ID = 1_000_000_001

_SOME_MESSAGE_ID = 4
_SOME_MESSAGE_DATA = {
    "id": 4,
    "subject": "Commodo reprehenderit",
    "body": "Id occaecat commodo reprehenderit aliqua Lorem nulla magna ea ipsum adipisicing.",
    "created_at": "2020-06-02 19:59:59",
    "is_read": False,
    "sender": {"email": "leon@test.com", "id": 3, "name": "Leon"},
}


def test_messages_post(app):
    access_token = create_access_token(identity=_SOME_USER_ID)

    response = app.post(
        "/api/messages",
        json={
            "subject": "Test Post URL",
            "body": "Lorem ipsum test!!",
            "recipient": _SOME_RECIPIENT_ID,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 201

    data = response.get_json()
    assert data["id"] == _DEFAULT_LENGTH_OF_MESSAGES_TABLE + 1  # should be 6
    # TODO: use freezegun to check created_at
    assert data["created_at"] is not None


@pytest.mark.parametrize(
    "json, expected",
    [
        (
            {"subject": "Test post fails", "recipient": _SOME_RECIPIENT_ID},
            {"body": ["Missing data for required field."]},
        ),
        (
            {"subject": "Test post fails", "body": "Lorem ipsum..."},
            {"recipient": ["Missing data for required field."]},
        ),
        (
            {
                "subject": "Test post fails",
                "body": "Lorem ipsum...",
                "recipient": _SOME_NON_EXISTING_ID,
            },
            "Recipient is not found.",
        ),
    ],
)
def test_messages_post_fails(json, expected, app):
    access_token = create_access_token(identity=_SOME_USER_ID)
    response = app.post(
        "/api/messages", json=json, headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 400
    assert response.get_json()["messages"] == expected


@pytest.mark.parametrize(
    "params, expected",
    [
        ({}, _SOME_USER_MESSAGES_IDS_AS_RECIPIENT),
        ({"is_read": 0}, _UNREAD_SOME_USER_MESSAGES_IDS_AS_RECIPIENT),
        ({"is_read": 1}, _READ_SOME_USER_MESSAGES_IDS_AS_RECIPIENT),
        ({"recipient": _SOME_RECIPIENT_ID}, _SOME_RECIPIENT_MESSAGES_IDS_AS_RECIPIENT),
        (
            {"recipient": _SOME_RECIPIENT_ID, "is_read": 0},
            _UNREAD_SOME_RECIPIENT_MESSAGES_IDS_AS_RECIPIENT,
        ),
        (
            {"recipient": _SOME_RECIPIENT_ID, "is_read": 1},
            _READ_SOME_RECIPIENT_MESSAGES_IDS_AS_RECIPIENT,
        ),
        # provide non existing values or keys
        ({"recipient": _SOME_NON_EXISTING_ID}, set()),
        # ignores this key
        ({"non-existing-field": _SOME_NON_EXISTING_ID}, _SOME_USER_MESSAGES_IDS_AS_RECIPIENT,),
    ],
)
def test_messages_by_args(params, expected, app):
    access_token = create_access_token(identity=_SOME_USER_ID)
    q = r"&".join([f"{k}={v}" for k, v in params.items()])

    response = app.get(f"/api/messages?{q}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

    messages = response.get_json()
    assert {message["id"] for message in messages} == expected


def test_messages_find_by_id(app):
    access_token = create_access_token(identity=_SOME_USER_ID)
    response = app.get(
        f"/api/messages/{_SOME_MESSAGE_ID}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.get_json() == _SOME_MESSAGE_DATA


def test_messages_find_by_id_missing(app):
    access_token = create_access_token(identity=_SOME_USER_ID)
    response = app.get(
        f"/api/messages/{_SOME_NON_EXISTING_ID}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 404
    assert (
        response.get_json()["messages"]
        == f"Message with this id: `{_SOME_NON_EXISTING_ID}` is not exists."
    )


@pytest.mark.parametrize("user_id", [_SOME_USER_ID, _SOME_RECIPIENT_ID])
def test_delete_message(user_id, app):
    access_token = create_access_token(identity=user_id)
    response = app.delete(
        f"/api/messages/{_SOME_USER_MESSAGE_ID_AS_OWNER}",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204


def test_delete_message_fails(app):
    access_token = create_access_token(identity=_SOME_USER_ID)
    response = app.delete(
        f"/api/messages/{_SOME_MESSAGE_ID}", headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 204
