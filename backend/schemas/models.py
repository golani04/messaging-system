from datetime import datetime
from typing import Dict

from marshmallow import fields, post_dump

from backend import ma
from backend.models import messages, users

from backend.const import DATETIME_FORMAT


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = users.User
        load_only = ("password",)
        include_population = True


class MessageSchema(ma.SQLAlchemyAutoSchema):
    sender = fields.Nested(UserSchema, only=("id", "name", "email"))

    @post_dump
    def _post_dump(self, data: Dict, *args, **kwargs):
        # convert from timestamp to utc datetime
        data["created_at"] = datetime.utcfromtimestamp(data["created_at"])
        return data

    class Meta:
        model = messages.Message
        load_only = ("owner",)
        datetimeformat = DATETIME_FORMAT
        include_fk = True
        include_population = True
