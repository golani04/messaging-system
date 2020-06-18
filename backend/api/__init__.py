from flask import Blueprint

bp = Blueprint("api", __name__)


# prevent circular imports
from . import users, messages, auth  # noqa: E402,F401
