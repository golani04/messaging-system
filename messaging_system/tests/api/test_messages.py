import pytest


def test_messages_post(app):
    response = app.post(
        "/api/messages",
        json={"body": "Lorem ipsum test!!", "subject": "Test Post URL", "owner": 3, "recipient": 1},
    )

    assert response.status_code == 200
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
