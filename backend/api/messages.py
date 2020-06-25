from flask import jsonify
from flask_jwt_extended import current_user, jwt_required
from webargs.flaskparser import use_kwargs

from backend.models.exceptions import DeleteError, SaveError, ValidationError
from backend.models.messages import Message
from backend.models.users import User

from backend.schemas.argumets import PostMessageSchema, SearchMessagesSchema
from backend.schemas.models import MessageSchema

from . import bp, errors, utils


@bp.route("/messages", methods=["POST"])
@jwt_required
@use_kwargs(PostMessageSchema)
def create_new_message(recipient: int, subject, body: str = "Lorem"):
    if (recipient := User.find_by_id(recipient)) is None:
        return errors.bad_request("Recipient is not found.")

    try:
        message = Message.create(subject, body, current_user.id)
        message.recipients.append(recipient)
        message.save()
    except SaveError as err:
        return errors.internal_error(err.messages)

    return MessageSchema().dump(message), 201


@bp.route("/messages", methods=["GET"])
@jwt_required
@use_kwargs(SearchMessagesSchema, location="query")
# TODO: add user role in order to find all messages sent by the specific user. Only admin
def get_messages(**search_params):
    search_params.setdefault("recipient", current_user.id)

    if search_params["recipient"] != current_user.id:
        # find my messages to the recipient
        search_params["owner"] = current_user.id

    messages = Message.filter_by(search_params)
    result = MessageSchema(many=True).dump(messages)

    return jsonify(result), 200


# TODO: using python-slugify use instead of <user_id>
#       use slugify(messages.subject-random-number)
@bp.route("/messages/<int:id>", methods=["GET"])
@jwt_required
@utils.check_item_exists(Message)
def get_message(result: Message):
    return MessageSchema().dump(result), 200


@bp.route("/messages/<int:id>", methods=["DELETE"])
@jwt_required
@utils.check_item_exists(Message)
def delete_message(result: Message):
    try:
        result.delete(current_user)
        return jsonify(), 204
    except (DeleteError, ValidationError) as err:
        return errors.internal_error(err.messages)
