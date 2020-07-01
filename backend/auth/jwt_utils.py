from flask import Response, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_csrf_token,
    set_access_cookies,
    set_refresh_cookies,
)

from backend.models.users import User


def response_with_tokens(user: User) -> Response:
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    response = make_response(
        {
            "access_csrf": get_csrf_token(access_token),
            "refresh_csrf": get_csrf_token(refresh_token),
        }
    )
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


def refresh_access_token(user: User) -> Response:
    access_token = create_access_token(identity=user.id)
    response = make_response({"access_csrf": get_csrf_token(access_token)})
    set_access_cookies(response, access_token)

    return response
