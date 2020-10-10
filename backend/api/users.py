from flask_jwt_extended import current_user, jwt_required

from backend.api import bp, errors, utils
from backend.api.auth import admin_required
from backend.models.exceptions import DeleteError, SaveError
from backend.models.users import User, UserRoles
from backend.schemas.argumets import CreateUserSchema, SearchUsersSchema
from backend.schemas.error import DefaultErrorSchema, ValidationErrorSchema
from backend.schemas.models import UserSchema


# TODO: using python-slugify use instead of <user_id> use slugify(user.name-random-number)
@bp.route("/users", methods=["GET"])
@bp.arguments(schema=SearchUsersSchema, location="query", as_kwargs=True)
@bp.response(
    schema=UserSchema(many=True, exclude=("password", "messages_sent", "messages_received")),
    code=200,
    description="Return users",
)
@bp.doc(
    summary="Get users",
    description="Return users or search by some values",
    responses={
        "200": {
            "schema": UserSchema(
                many=True, exclude=("password", "messages_sent", "messages_received")
            ),
            "description": "Return users",
        },
        "400": {
            "schema": ValidationErrorSchema,
            "description": "Incorrect types of argument values",
        },
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@jwt_required
def get_users(**search_params):
    users = User.filter_by(current_user.id, search_params)
    if current_user.role != UserRoles.admin:
        # TODO: implement address book
        pass

    return users, 200


@bp.route("/users", methods=["POST"])
@bp.arguments(schema=CreateUserSchema, description="Create a new user", as_kwargs=True)
@bp.response(
    schema=UserSchema(exclude=("password", "messages_sent", "messages_received")),
    code=201,
    description="Return a new user",
)
@bp.doc(
    summary="Create a new user",
    description="Create a new user, admin action.",
    responses={
        "201": {
            "schema": UserSchema(exclude=("password", "messages_sent", "messages_received")),
            "description": "Return a new user",
        },
        "400": {"schema": ValidationErrorSchema, "description": "Incorrect types "},
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "500": {"schema": DefaultErrorSchema, "description": "Failed to create a  new user"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@admin_required
def create_user(name, email, password: str):
    if User.autenticate(email) is not None:
        return errors.bad_request({"email": "Email is already exists."})
    try:
        new_user = User.create(name, email, password)
        new_user.save()
    except SaveError as err:
        return errors.internal_error(err.messages)

    return new_user, 201


@bp.route("/users/<int:id>", methods=["GET"])
@bp.response(
    schema=UserSchema(exclude=("password", "messages_sent", "messages_received")),
    code=200,
    description="Using an id get the user",
)
@bp.doc(
    summary="Return a user by id",
    description="Return a user by id",
    responses={
        "200": {
            "schema": UserSchema(exclude=("password", "messages_sent", "messages_received")),
            "description": "User is found",
        },
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "404": {"schema": DefaultErrorSchema, "description": "User is not found"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@jwt_required
@utils.check_item_exists(User)
def get_user(user: User):
    if current_user.role != UserRoles.admin:
        # TODO: implement address book
        pass

    # return only messages between this user and current_user
    # TODO: how to filter relationships props
    return user, 200


@bp.route("/users/<int:id>", methods=["PATCH"])
@bp.arguments(schema=CreateUserSchema(partial=True), as_kwargs=True)
@bp.response(code=204, description="User successfully updated")
@bp.doc(
    summary="Update a user properties",
    description="Update a user properties. Only admin can update other users.",
    responses={
        "400": {"schema": ValidationErrorSchema, "description": "Validation errors"},
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "403": {"schema": DefaultErrorSchema, "description": "You can't modify other users"},
        "404": {"schema": DefaultErrorSchema, "description": "User is not found"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@jwt_required
@utils.check_item_exists(User)
def update_user(user: User, **params):
    if not params:
        return errors.error_response(200, "Nothing to update missing properties")

    if current_user.id != user.id and current_user.role != UserRoles.admin:
        return errors.forbidden("User can modify only his properties.")

    try:
        user.update(params)
        user.save()
    except SaveError as err:
        return errors.internal_error(err.messages)

    return {}, 204


@bp.route("/users/<int:id>", methods=["DELETE"])
@bp.response(code=204, description="User is successfully deleted")
@bp.doc(
    summary="Delete a user",
    description="Delete user by id, admin allowed actions",
    responses={
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "403": {"schema": DefaultErrorSchema, "description": "Admin action required"},
        "404": {"schema": DefaultErrorSchema, "description": "User is not found"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@admin_required
@utils.check_item_exists(User)
def delete_user(user: User):
    try:
        user.delete()
        return {}, 204
    except DeleteError as err:
        return errors.internal_error(err.messages), 200
