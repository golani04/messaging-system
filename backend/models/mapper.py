from backend import db

from . import messages, validate

__tablename__ = "UserMessages"


def create_ref(message: messages.Message, recipient: int) -> id:
    """Create reference between message and recipient."""

    if message.owner == recipient:
        raise validate.ValidationError("Recipient and owner can not be same person")

    rowid = db.insert(__tablename__, {"r_id": recipient, "m_id": message.id})

    if rowid > 0:
        return rowid

    # m_id should be always correct,
    # Message.create will catch an error and throw a validation error before this called
    raise validate.ValidationError("Recipient is not exits.")
