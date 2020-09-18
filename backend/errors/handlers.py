from collections import defaultdict

from backend.api import errors
from backend.errors import bp


@bp.app_errorhandler(422)
def entity_unprocessable(err):
    error_msg = defaultdict(dict, err.data.get("messages", None))
    return errors.bad_request(error_msg["json"])
