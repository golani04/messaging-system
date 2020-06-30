import pytest


_SOME_USER_EMAIL = "janedoe@test.com"
_SOME_USER_PASSWORD = "password"
_SOME_NON_EXISTING_EMAIL = "nonexsting@nonexsting.com"
_SOME_NON_EXISTING_PASSWORD = "jlasflksjadf-sadfsadf.sdaf"


def test_auth_login(app):
    response = app.post(
        "/auth/login", json={"email": _SOME_USER_EMAIL, "password": _SOME_USER_PASSWORD}
    )
    assert response.status_code == 200

    cookies = response.headers.getlist("Set-Cookie")
    assert any(cookie.startswith("access_token") for cookie in cookies)

    tokens = response.get_json()
    assert "access_csrf" in tokens


@pytest.mark.parametrize(
    "json, expected",
    [
        ({"email": _SOME_USER_EMAIL}, (400, {"password": ["Missing data for required field."]})),
        (
            {"email": _SOME_NON_EXISTING_EMAIL, "password": _SOME_USER_PASSWORD},
            (404, "Couldn't find an account with this email."),
        ),
        (
            {"email": _SOME_USER_EMAIL, "password": _SOME_NON_EXISTING_PASSWORD},
            (401, "The email and password did not match our records."),
        ),
    ],
)
def test_auth_login_fails(json, expected, app):
    response = app.post("/auth/login", json=json)

    status_code, expected_messages = expected

    assert response.status_code == status_code
    error = response.get_json()

    assert error["messages"] == expected_messages
