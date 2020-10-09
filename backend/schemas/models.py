from datetime import datetime
from typing import Dict

from marshmallow import EXCLUDE, fields, post_dump
from marshmallow.validate import Length

from backend import ma
from backend.const import DATETIME_FORMAT
from backend.models import messages, users


class UserSchema(ma.SQLAlchemyAutoSchema):
    email = fields.Email(required=True)
    password = fields.String(
        validate=Length(min=8, error="Short password. Minimum {min} characters."), required=True
    )

    messages_sent = fields.Nested("MessageSchema", exclude=("sender",), many=True)
    messages_received = fields.Nested("MessageSchema", many=True)

    @post_dump
    def post_dump(self, data, *args, **kwargs):
        if "role" in data:
            data["role"] = users.UserRoles(data["role"]).name

        return data

    class Meta:
        model = users.User
        unknown = EXCLUDE
        include_relationships = True
        load_only = ("password",)


class MessageSchema(ma.SQLAlchemyAutoSchema):
    sender = fields.Nested(UserSchema, only=("id", "name", "email"))

    @post_dump
    def _post_dump(self, data: Dict, *args, **kwargs):
        # convert from timestamp to utc datetime
        data["created_at"] = datetime.utcfromtimestamp(data["created_at"])
        return data

    class Meta:
        model = messages.Message
        include_fk = True
        datetimeformat = DATETIME_FORMAT
        load_only = ("owner",)
        dump_only = ("sender",)
