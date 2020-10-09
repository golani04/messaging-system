from flask import jsonify
from flask_jwt_extended import current_user, jwt_required

from backend.api import bp, errors, utils
from backend.models.exceptions import DeleteError, SaveError, ValidationError
from backend.models.messages import Message
from backend.models.users import User
from backend.schemas.argumets import PostMessageSchema, SearchMessagesSchema
from backend.schemas.error import DefaultErrorSchema, ValidationErrorSchema
from backend.schemas.models import MessageSchema


@bp.route("/messages", methods=["POST"])
@bp.arguments(
    schema=PostMessageSchema,
    description="Send a new message",
    example={"subject": "Test Post URL", "body": "Lorem ipsum test!!", "recipient": 1},
    as_kwargs=True,
)
@bp.response(schema=MessageSchema, code=201, description="Return a created message")
@bp.doc(
    summary="Send a new message",
    description="Send a new message to the recipient using an id",
    responses={
        "201": {"schema": MessageSchema, "description": "Return a created message"},
        "400": {"schema": ValidationErrorSchema, "description": "Missing a recipient"},
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "500": {"schema": DefaultErrorSchema, "description": "Failed to send a message"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@jwt_required
def create_new_message(recipient: int, subject="Lorem", body: str = "Lorem"):
    if (recipient := User.find_by_id(recipient)) is None:
        return errors.bad_request("Recipient is not found.")

    try:
        message = Message.create(subject, body, current_user.id)
        message.recipients.append(recipient)
        message.save()
    except SaveError as err:
        return errors.internal_error(err.messages)

    return message, 201


@bp.route("/messages", methods=["GET"])
@bp.arguments(SearchMessagesSchema, location="query", as_kwargs=True)
@bp.response(schema=MessageSchema(many=True), code=200, description="Get or search messages")
@bp.doc(
    summary="Search messages or return user's messages",
    description=(
        "if recipient is not user return user's messages to the recipient "
        "or messages sent to user by others"
    ),
    responses={
        "200": {
            "schema": MessageSchema(many=True),
            "description": "Return found messages to or from user",
        },
        "400": {"schema": ValidationErrorSchema, "description": "Incorrect types argument values"},
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@jwt_required
def get_messages(**search_params):
    # TODO: add user role in order to find all messages sent by the specific user. Only admin
    search_params.setdefault("recipient", current_user.id)

    if search_params["recipient"] != current_user.id:
        # find my messages to the recipient
        search_params["owner"] = current_user.id

    messages = Message.filter_by(search_params)

    return messages, 200


# TODO: using python-slugify use instead of <user_id>
#       use slugify(messages.subject-random-number)
@bp.route("/messages/<int:id>", methods=["GET"])
@bp.response(schema=MessageSchema, code=200, description="Return user message by id")
@bp.doc(
    summary="Return a message by message id",
    description="Return a message by message id",
    responses={
        "200": {"schema": MessageSchema, "description": "Message is found"},
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "404": {"schema": DefaultErrorSchema, "description": "Message is not found"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@jwt_required
@utils.check_item_exists(Message)
def get_message(result: Message):
    return result, 200


@bp.route("/messages/<int:id>", methods=["DELETE"])
@bp.response(code=204, description="Message successfuly deleted")
@bp.doc(
    summary="Delete message by given message id",
    description="Delete message by given message id",
    responses={
        "401": {"schema": DefaultErrorSchema, "description": "Wrong credentials"},
        "404": {"schema": DefaultErrorSchema, "description": "Message is not found"},
        "default": {"schema": DefaultErrorSchema, "description": "Default errors"},
    },
)
@jwt_required
@utils.check_item_exists(Message)
def delete_message(result: Message):
    try:
        result.delete(current_user)
        return jsonify(), 204
    except (DeleteError, ValidationError) as err:
        return errors.internal_error(err.messages)
