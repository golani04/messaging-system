from flask import Blueprint

bp = Blueprint("auth", __name__)

# prevent circular imports
from . import auth  # noqa: E402,F401
