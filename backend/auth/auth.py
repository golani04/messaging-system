from flask_jwt_extended import current_user, jwt_refresh_token_required, jwt_required
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
    #       Add dummy password to run verify password function to prevent timing attack
    if user is None:
        return errors.not_found("Couldn't find an account with this email.")

    if not user.verify_passw(password, user.password):
        return errors.unauthorized("The email and password did not match our records.")

    return jwt_utils.response_with_tokens(user), 200


@bp.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh_access_token():
    return jwt_utils.refresh_access_token(current_user), 200


@bp.route("/logout", methods=["POST"])
@jwt_required
def logout():
    return jwt_utils.logout_user(), 204


# TODO: Blacklist tokens
# https://github.com/vimalloc/flask-jwt-extended/tree/master/examples/database_blacklist

# TODO: Forgot password
# https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
