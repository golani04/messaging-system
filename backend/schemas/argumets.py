from marshmallow import Schema, ValidationError, fields, pre_load, EXCLUDE
from .models import MessageSchema


class PostMessageSchema(Schema):
    recipient = fields.Integer(required=True)

    @pre_load
    def _pre_load(self, data, *_args, **_kwargs):
        schema = MessageSchema(unknown=EXCLUDE, only=self.opts.additional)
        if errors := schema.validate(data):
            raise ValidationError(errors)

        return data

    class Meta:
        unknown = EXCLUDE
        additional = ("subject", "body")


class SearchMessagesSchema(Schema):
    recipient = fields.Integer()

    @pre_load
    def _pre_load(self, data, *_args, **_kwargs):
        schema = MessageSchema(unknown=EXCLUDE, only=self.opts.additional)
        if errors := schema.validate(data, partial=True):
            raise ValidationError(errors)

        return data

    class Meta:
        unknown = EXCLUDE
        additional = ("created_at", "is_read", "owner", "subject")
