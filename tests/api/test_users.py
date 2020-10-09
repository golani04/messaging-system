import pytest
from flask_jwt_extended import create_access_token

_SOME_USER_ID = 1
_SOME_USER_EMAIL = "janedoe@test.com"
_SOME_USER_PASSWORD = "password"
_SOME_OTHER_USER_ID = 2
_SOME_ADMIN_USER_ID = 3
_DEFAULT_USERS_IDS = {1, 2, 3}

_SOME_NEW_EMAIL = "tester@test.com"
_SHORT_PASSWORD = "passw"
_NON_EXISTING_ID = 1_000_000_001


@pytest.mark.parametrize("user_id", [_SOME_USER_ID, _SOME_ADMIN_USER_ID])
def test_get_users(user_id, app):
    access_token = create_access_token(identity=user_id)
    response = app.get("/api/users", headers={"Authorization": f"Bearer {access_token}"})

    assert response.status_code == 200

    users = response.get_json()
    assert {user["id"] for user in users} == {id_ for id_ in _DEFAULT_USERS_IDS if id_ != user_id}


def test_create_user(app):
    access_token = create_access_token(identity=_SOME_ADMIN_USER_ID)
    response = app.post(
        "/api/users",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Leon", "email": _SOME_NEW_EMAIL, "password": "monster-password"},
    )

    assert response.status_code == 201
    user = response.get_json()
    assert user.get("password") is None
    assert user["id"] == len(_DEFAULT_USERS_IDS) + 1


@pytest.mark.parametrize(
    "values, expected",
    [
        (
            (_SOME_USER_EMAIL, _SOME_USER_PASSWORD, _SOME_ADMIN_USER_ID),
            {"email": "Email is already exists."},
        ),
        (
            (_SOME_NEW_EMAIL, _SHORT_PASSWORD, _SOME_ADMIN_USER_ID),
            {"password": ["Short password. Minimum 8 characters."]},
        ),
        (
            (_SOME_NEW_EMAIL, _SOME_USER_PASSWORD, _SOME_USER_ID),  # 403
            "Create or delete an user can only be performed by the admin!",
        ),
    ],
)
def test_create_user_fails(values, expected, app):
    email, password, current_user_id = values
    access_token = create_access_token(identity=current_user_id)
    response = app.post(
        "/api/users",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Leon", "email": email, "password": password},
    )

    assert response.status_code in {400, 403}
    assert response.get_json()["errors"] == expected


def test_get_user(app):
    access_token = create_access_token(identity=_SOME_USER_ID)
    response = app.get(
        f"/api/users/{_SOME_OTHER_USER_ID}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "id": _SOME_OTHER_USER_ID,
        "name": "John",
        "email": "johndoe@test.com",
        "role": "user",
    }


def test_get_user_fails(app):
    access_token = create_access_token(identity=_SOME_USER_ID)
    response = app.get(
        f"/api/users/{_NON_EXISTING_ID}", headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 404
    assert (
        response.get_json()["errors"] == f"User with this id: `{_NON_EXISTING_ID}` is not exists."
    )


@pytest.mark.parametrize("user_id", [_SOME_ADMIN_USER_ID, _SOME_USER_ID])
def test_update_user(user_id, app):
    access_token = create_access_token(identity=user_id)
    response = app.patch(
        f"/api/users/{_SOME_USER_ID}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"email": _SOME_NEW_EMAIL},
    )

    assert response.status_code == 204


def test_update_user_fails(app):
    access_token = create_access_token(identity=_SOME_USER_ID)
    response = app.patch(
        f"/api/users/{_SOME_USER_ID}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"id": _NON_EXISTING_ID},
    )

    assert response.status_code == 200
    assert response.get_json()["errors"] == "Nothing to update missing properties"


def test_update_user_fails_to_update_other_user(app):
    access_token = create_access_token(identity=_SOME_USER_ID)
    response = app.patch(
        f"/api/users/{_SOME_OTHER_USER_ID}",
        headers={"Authorization": f"Bearer {access_token}"},
        json={"name": "Some name"},
    )

    assert response.status_code == 403
    assert response.get_json()["errors"] == "User can modify only his properties."


def test_delete_user_by_admin(app):
    access_token = create_access_token(identity=_SOME_ADMIN_USER_ID)
    response = app.delete(
        f"/api/users/{_SOME_USER_ID}", headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 204

    # insure that user with this id was deleted
    response = app.get(
        f"/api/users/{_SOME_USER_ID}", headers={"Authorization": f"Bearer {access_token}"},
    )
    assert response.status_code == 404


def test_delete_user_by_admin_fails(app):
    access_token = create_access_token(identity=_SOME_USER_ID)
    response = app.delete(
        f"/api/users/{_SOME_USER_ID}", headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403
    assert (
        response.get_json()["errors"]
        == "Create or delete an user can only be performed by the admin!"
    )
