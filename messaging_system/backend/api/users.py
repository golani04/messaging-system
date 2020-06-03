from flask import jsonify, request

from backend.models.users import User
from . import bp


@bp.route("/users/<int:user_id>/messages", methods=["GET"])
def get_messages_from_user(user_id: int):
    user = User.find_by_id(user_id)
    if user is None:
        return jsonify([])

    result = user.get_messages(request.args)
    return jsonify([item.to_json() for item in result])
