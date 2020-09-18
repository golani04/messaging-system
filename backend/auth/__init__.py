from flask import Blueprint

from backend import secure_headers

bp = Blueprint("auth", __name__)


@bp.after_request
def after_request(response):
    # adding additional secure headers
    secure_headers.flask(response)
    return response


# prevent circular imports
from . import auth  # noqa: E402,F401
