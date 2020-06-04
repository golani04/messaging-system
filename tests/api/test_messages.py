import pytest

from backend.models.messages import Message


def test_messages_post(app):
    response = app.post(
        "/api/messages",
        json={"body": "Lorem ipsum test!!", "subject": "Test Post URL", "owner": 3, "recipient": 1},
    )

    assert response.status_code == 201
    res = response.get_json()
    assert res["id"] > 0
    # TODO: use freezegun to check created_at
    assert res["created_at"] is not None


@pytest.mark.parametrize(
    "params, expected", [({}, 5), ({"recipient": 1}, 2), ({"recipient": 1, "is_read": False}, 0)]
)
def test_messages_by_args(params, expected, app):
    q = r"&".join([f"{k}={v}" for k, v in params.items()])
    response = app.get(f"/api/messages?{q}")

    assert response.status_code == 200
    assert len(response.get_json()) == expected


def test_messages_by_args_loggedin(app):
    response = app.post("/auth/login", json={"email": "janedoe@test.com", "password": "password"})
    access_token = response.get_json()["access_token"]

    assert response.status_code == 200
    assert access_token is not None

    response = app.get("/api/messages", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200

    messages_via_api = response.get_json()
    messages_via_db = Message.filter_by({"recipient": 1})

    assert {item["id"] for item in messages_via_api} == {item.id for item in messages_via_db}


@pytest.mark.parametrize("params", [{"recipient": 10001}, {"non-existing-field": 10001}])
def test_messages_by_args_fails(params, app):
    q = r"&".join([f"{k}={v}" for k, v in params.items()])
    response = app.get(f"/api/messages?{q}")

    assert response.status_code == 200
    assert response.get_json() == []


def test_find_by_id(app):
    response = app.get("/api/messages/4")

    assert response.status_code == 200
    assert set(response.get_json()) >= {"id", "created_at", "owner", "body", "subject"}


def test_find_by_id_missing(app):
    response = app.get("/api/messages/100000001")

    assert response.status_code == 404
    assert response.get_json()["message"] == "Searched message: 100000001 is not exists."


def test_delete_message(app):
    response = app.delete("/api/messages/1")
    assert response.status_code == 204
