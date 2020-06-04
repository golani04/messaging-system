from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import jwt_optional, get_jwt_identity

from backend import db
from backend.models import mapper, validate
from backend.models.messages import Message

from . import bp, errors


def check_item_exists(f):
    @wraps(f)
    def wrapper(m_id: int):
        message = Message.find_by_id(m_id)

        if message is None:
            return errors.not_found(f"Searched message: {m_id} is not exists.")

        return f(message)

    return wrapper


@bp.route("/messages", methods=["POST"])
def create_new_message():
    json = request.get_json()
    if not json:
        return errors.bad_request("Missing data")

    # NOTE: if project has a lot of this functionalite best to use a decorator
    required_keys = {"body", "subject", "owner", "recipient"}
    keys = set(json)
    if not required_keys <= keys:
        return errors.bad_request(f"Missing keys: {required_keys - keys}")

    recipient = json.pop("recipient")
    try:
        message = Message(**json)
        with db.conn:
            message.create()
            mapper.create_ref(message, recipient)

        message.save()
    except validate.ValidationError as err:
        return errors.bad_request(err.messages)

    return jsonify(message.to_json()), 201


@bp.route("/messages", methods=["GET"])
@jwt_optional
def get_messages():
    args = request.args
    user_id = get_jwt_identity()

    if user_id is not None:
        args = {**args, "recipient": user_id}

    result = Message.filter_by(args)
    return jsonify([item.to_json() for item in result])


@bp.route("/messages/<int:m_id>", methods=["GET"])
@check_item_exists
def get_message(result: Message):
    # NOTE: this api will also set is_read to True as a side effect
    # TODO: consider different approach
    result.save()
    return jsonify(result.to_json())


@bp.route("/messages/<int:m_id>", methods=["DELETE"])
@check_item_exists
def delete_message(result: Message):
    if result.delete():
        result.save()
        return jsonify(), 204

    return errors.bad_request(f"Deleting item `{result.id}` was not successful.")
