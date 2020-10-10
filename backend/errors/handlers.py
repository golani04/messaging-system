from marshmallow import ValidationError
from collections import defaultdict

from backend.api import errors
from backend.errors import bp


@bp.app_errorhandler(400)
def catch_default_errors(err):
    if isinstance(err.exc, ValidationError):
        error_msg = defaultdict(dict, err.data.get("messages", None))
        return errors.bad_request(error_msg["json"])

    return errors.bad_request(err.data)
