from flask import jsonify
from flask_jwt_extended import jwt_required, current_user
from marshmallow import EXCLUDE
from webargs.flaskparser import use_kwargs

from backend.api.auth import admin_required
from backend.models.users import User, UserRoles
from backend.models.exceptions import DeleteError, SaveError
from backend.schemas.models import UserSchema
from backend.schemas.argumets import SearchUsersSchema

from . import bp, errors, utils


# TODO: using python-slugify use instead of <user_id> use slugify(user.name-random-number)
@bp.route("/users", methods=["GET"])
@jwt_required
@use_kwargs(SearchUsersSchema, location="query")
def get_users(**search_params):
    users = User.filter_by(current_user.id, search_params)
    if current_user.role != UserRoles.admin:
        # TODO: implement address book
        pass

    return jsonify(UserSchema(many=True, only=("id", "name", "email", "role")).dump(users)), 200


@bp.route("/users", methods=["POST"])
@admin_required
@use_kwargs(UserSchema)
def create_user(name, email, password: str):
    if User.autenticate(email) is not None:
        return errors.bad_request({"email": "Email is already exists."})
    try:
        new_user = User.create(name, email, password)
        new_user.save()
    except SaveError as err:
        return errors.internal_error(err.messages)

    return jsonify(UserSchema().dump(new_user)), 201


@bp.route("/users/<int:id>", methods=["GET"])
@jwt_required
@utils.check_item_exists(User)
def get_user(user: User):
    if current_user.role != UserRoles.admin:
        # TODO: implement address book
        pass

    # return only messages between this user and current_user
    # TODO: how to filter relationships props
    return jsonify(UserSchema(exclude=("messages_sent", "messages_received")).dump(user)), 200


@bp.route("/users/<int:id>", methods=["PATCH"])
@jwt_required
# define dynamicaly allowed keys in schema
@use_kwargs(UserSchema(partial=True, only=("name", "email", "password"), unknown=EXCLUDE))
@utils.check_item_exists(User)
def update_user(user: User, **params):
    if current_user.id != user.id and current_user.role != UserRoles.admin:
        return errors.unauthorized("User can modify only himself.")

    try:
        user.update(params)
        user.save()
    except SaveError as err:
        return errors.internal_error(err.messages)

    return jsonify(UserSchema().dump(user)), 200


@bp.route("/users/<int:id>", methods=["DELETE"])
@admin_required
@utils.check_item_exists(User)
def delete_user(user: User):
    try:
        user.delete()
        return {}, 204
    except DeleteError as err:
        return errors.internal_error(err.messages), 200
