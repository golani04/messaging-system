from flask_smorest.blueprint import Blueprint

from backend import secure_headers

bp = Blueprint("auth", __name__)
# default validation status override
bp.ARGUMENTS_PARSER.DEFAULT_VALIDATION_STATUS = 400


@bp.after_request
def after_request(response):
    # adding additional secure headers
    secure_headers.flask(response)
    return response


# prevent circular imports
from backend.auth import auth  # noqa: E402,F401
