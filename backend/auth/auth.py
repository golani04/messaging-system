from flask_jwt_extended import current_user, jwt_refresh_token_required, jwt_required
from marshmallow import EXCLUDE

from backend import jwt
from backend.api import errors
from backend.auth import bp, jwt_utils
from backend.models.users import User
from backend.schemas.argumets import CreateUserSchema, LoginSchema
from backend.schemas.error import DefaultErrorSchema, ValidationErrorSchema
from backend.schemas.responses import AccessTokenSchema, TokensSchema


@jwt.invalid_token_loader
def invalid_token(*args, **kwargs):
    return errors.unauthorized("Unathorized")


@bp.route("/register", methods=["POST"])
@bp.arguments(schema=CreateUserSchema(unknown=EXCLUDE), as_kwargs=True)
@bp.doc(
    summary="Register",
    description="Register a new users",
    responses={
        "201": {"description": "User is successfully registered", "schema": TokensSchema},
        "400": {
            "schema": ValidationErrorSchema,
            "description": "Incorrect types of argument values",
        },
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
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
@bp.arguments(schema=LoginSchema(unknown=EXCLUDE), as_kwargs=True)
@bp.doc(
    summary="Login",
    description="Login",
    responses={
        "200": {"description": "User is successfully registered", "schema": TokensSchema},
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "400": {
            "schema": ValidationErrorSchema,
            "description": "Incorrect types of argument values",
        },
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
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
@bp.doc(
    summary="Generate a new access_token",
    description="Generate a new access_token",
    responses={
        "200": {"description": "Return newly generated access token", "schema": AccessTokenSchema},
        "401": {"schema": DefaultErrorSchema, "description": "Wrong refresh token"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@jwt_refresh_token_required
def refresh_access_token():
    return jwt_utils.refresh_access_token(current_user), 200


@bp.route("/logout", methods=["POST"])
@bp.response(code=204, description="Logout from application")
@bp.doc(
    summary="Logout",
    description="Logout from application",
    responses={
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@jwt_required
def logout():
    return jwt_utils.logout_user(), 204


# TODO: Blacklist tokens
# https://github.com/vimalloc/flask-jwt-extended/tree/master/examples/database_blacklist

# TODO: Forgot password
# https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html
