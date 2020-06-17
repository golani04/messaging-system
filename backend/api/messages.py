from functools import wraps

from flask import jsonify
from flask_jwt_extended import current_user, jwt_required
from webargs.flaskparser import use_kwargs

from backend import jwt
from backend.models.exceptions import DeleteError, SaveError, ValidationError
from backend.models.messages import Message
from backend.models.users import User

from backend.schemas.argumets import PostMessageSchema, SearchMessagesSchema
from backend.schemas.models import MessageSchema

from . import bp, errors


def check_item_exists(f):
    @wraps(f)
    def wrapper(m_id: int):
        message = Message.find_by_id(m_id)

        if message is None:
            return errors.not_found(f"Searched message: {m_id} is not exists.")

        return f(message)

    return wrapper


@jwt.user_loader_callback_loader
def load_user(identity):
    # set current user
    return User.query.get(identity)


@bp.route("/messages", methods=["POST"])
@use_kwargs(PostMessageSchema)
@jwt_required
def create_new_message(recipient, subject, body="Lorem"):
    if (recipient := User.query.get(recipient)) is None:
        return errors.bad_request("Recipient is not found.")

    try:
        message = Message.create(subject, body, current_user.id)
        message.recipients.append(recipient)
        message.save()
    except SaveError as err:
        return errors.internal_error(err.messages)

    return MessageSchema().dump(message), 201


@bp.route("/messages", methods=["GET"])
@use_kwargs(SearchMessagesSchema, location="query")
@jwt_required
# TODO: add user role in order to find all messages sent by the specific user. Only admin
def get_messages(**search_params):
    search_params.setdefault("recipient", current_user.id)

    if search_params["recipient"] != current_user.id:
        # find my messages to the recipient
        search_params["owner"] = current_user.id

    messages = Message.filter_by(search_params)
    result = MessageSchema(many=True).dump(messages)

    return jsonify(result), 200


@bp.route("/messages/<int:m_id>", methods=["GET"])
@check_item_exists
@jwt_required
def get_message(result: Message):
    return MessageSchema().dump(result), 200


@bp.route("/messages/<int:m_id>", methods=["DELETE"])
@check_item_exists
@jwt_required
def delete_message(result: Message):
    try:
        result.delete(current_user)
        return jsonify(), 204
    except (DeleteError, ValidationError) as err:
        return errors.internal_error(err.messages)
