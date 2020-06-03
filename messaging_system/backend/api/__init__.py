from flask import Blueprint

bp = Blueprint("api", __name__)

# prevent circular imports
from .users import users  # noqa: E402,F401
from .messages import messages  # noqa: E402,F401
