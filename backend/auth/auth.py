from marshmallow import EXCLUDE
from webargs.flaskparser import use_kwargs

from backend.api import errors
from backend.models.users import User
from backend.schemas.models import UserSchema

from . import bp, jwt_utils


@bp.route("/register", methods=["POST"])
@use_kwargs(UserSchema(only=("name", "email", "password"), unknown=EXCLUDE))
def register(name: str, email: str, password: str):
    user = User.autenticate(email)
    if user is not None:
        return errors.bad_request(
            "User with this email is already in the system. Are you trying to logged in?"
        )

    user = User.create(name, email, password)
    user.save()

    return jwt_utils.response_with_tokens(user), 201


@bp.route("/login", methods=["POST"])
@use_kwargs(UserSchema(only=("email", "password"), unknown=EXCLUDE))
def login(email: str, password: str):
    user = User.autenticate(email)

    # TODO: if email is missing, using brute force to get existing users
    #       Consider limit number of tries or show 401 error Bad email or password
    if user is None:
        return errors.not_found("Couldn't find an account with this email.")

    if not user.verify_passw(password, user.password):
        return errors.unauthorized("The email and password did not match our records.")

    return jwt_utils.response_with_tokens(user), 200
