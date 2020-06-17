import pytest


def test_auth_login(app):
    response = app.post("/auth/login", json={"email": "janedoe@test.com", "password": "password"})

    assert response.status_code == 200
    payload = response.get_json()
    assert "access_token" in payload


@pytest.mark.parametrize(
    "json, expected",
    [
        ({"email": "janedoe@test.com"}, (400, "Missing email or password.")),
        (
            {"email": "nonexsting@nonexsting.com", "password": "password"},
            (404, "User with this email does not exist."),
        ),
        ({"email": "janedoe@test.com", "password": "wrong"}, (401, "Bad email or password.")),
    ],
)
def test_auth_login_fails(json, expected, app):
    response = app.post("/auth/login", json=json)

    assert response.status_code == expected[0]
    error = response.get_json()

    assert error["messages"] == expected[1]
