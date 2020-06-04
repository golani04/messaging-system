from flask import jsonify, request

from backend.models.users import User
from . import bp, errors


@bp.route("/users/<int:user_id>/messages", methods=["GET"])
def get_messages_from_user(user_id: int):
    user = User.find_by_id(user_id)
    if user is None:
        return jsonify([])

    result = user.get_messages(request.args)
    return jsonify([item.to_json() for item in result])


@bp.route("/users/<int:user_id>/messages/<int:message_id>", methods=["GET"])
def get_message_from_user(user_id: int, message_id: int):
    user = User.find_by_id(user_id)
    if user is None:
        return jsonify([])

    result = user.get_messages(request.args, message_id)
    if not result:
        return errors.not_found(f"User {user_id} has no message {message_id}.")

    return jsonify(result[0].to_json())
