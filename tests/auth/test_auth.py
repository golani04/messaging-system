from flask_jwt_extended import create_refresh_token, create_access_token, get_csrf_token

import pytest


_SOME_USER_ID = 1
_SOME_USER_EMAIL = "janedoe@test.com"
_SOME_USER_PASSWORD = "password"
_SOME_NON_EXISTING_EMAIL = "nonexsting@nonexsting.com"
_SOME_NON_EXISTING_PASSWORD = "jlasflksjadf-sadfsadf.sdaf"

_SOME_USER_NAME = "Test Tester"
_SOME_USER_NEW_EMAIL = "newuser@test.com"


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


def test_user_registration(app):
    response = app.post(
        "/auth/register",
        json={
            "email": _SOME_USER_NEW_EMAIL,
            "name": _SOME_USER_NAME,
            "password": _SOME_USER_PASSWORD,
        },
    )
    assert response.status_code == 201

    cookie = next(cookie for cookie in app.cookie_jar if cookie.name == "access_token_cookie")
    access_csrf = response.get_json()["access_csrf"]
    assert get_csrf_token(cookie.value) == access_csrf


@pytest.mark.parametrize(
    "data, expected",
    [
        (
            {"email": _SOME_USER_EMAIL, "name": _SOME_USER_NAME, "password": _SOME_USER_PASSWORD},
            "User with this email is already in the system. Are you trying to logged in?",
        ),
        (
            {"name": _SOME_USER_NAME, "password": _SOME_USER_PASSWORD},
            {"email": ["Missing data for required field."]},
        ),
    ],
)
def test_user_registration_fails(data, expected, app):
    response = app.post("/auth/register", json=data)

    assert response.status_code == 400
    assert response.get_json()["messages"] == expected


def test_refresh_token(app):
    refresh_token = create_refresh_token(identity=_SOME_USER_ID)
    response = app.post("/auth/refresh", headers={"Authorization": f"Bearer {refresh_token}"},)

    cookie = next(cookie for cookie in app.cookie_jar if cookie.name == "access_token_cookie")
    access_csrf = response.get_json()["access_csrf"]
    assert access_csrf == get_csrf_token(cookie.value)


def test_wrong_refresh_token(app):
    wrong_token = create_access_token(identity=_SOME_USER_ID)
    app.post("/auth/refresh", headers={"Authorization": f"Bearer {wrong_token}"})

    with pytest.raises(StopIteration):
        next(cookie for cookie in app.cookie_jar if cookie.name == "access_token_cookie")
