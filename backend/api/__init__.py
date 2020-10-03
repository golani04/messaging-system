from flask_smorest.blueprint import Blueprint

from backend import secure_headers

bp = Blueprint("api", __name__)


@bp.after_request
def after_request(response):
    # adding additional secure headers
    secure_headers.flask(response)
    return response


# prevent circular imports
from . import auth, messages, users  # noqa: E402,F401
