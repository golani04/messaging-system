from flask import jsonify, request

from backend import db
from backend.models import mapper, validate
from backend.models.messages import Message

from . import bp, errors


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
    except validate.ValidationError as err:
        return errors.bad_request(err)

    return jsonify(message.to_json()), 201


@bp.route("/messages", methods=["GET"])
def get_messages():
    result = Message.filter_by(request.args)

    return jsonify([item.to_json() for item in result])


@bp.route("/messages/<int:m_id>", methods=["GET"])
def get_message(m_id: int):
    result = Message.find_by_id(m_id)

    if result is None:
        return errors.not_found(f"Searched message: {m_id} is not exists.")

    return jsonify(result.to_json())
