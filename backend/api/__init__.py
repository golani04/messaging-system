from flask import Blueprint

bp = Blueprint("api", __name__)

# prevent circular imports
from . import users, messages  # noqa: E402,F401
