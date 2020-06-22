from functools import wraps
from flask_jwt_extended import current_user, verify_jwt_in_request

from backend import jwt
from backend.models.users import User, UserRoles

from .errors import forbidden


@jwt.user_loader_callback_loader
def load_user(identity):
    # set current user
    return User.query.get(identity)


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        if not current_user or current_user.role != UserRoles.admin:
            return forbidden("Create or delete an user can only be performed by the admin!")

        return fn(*args, **kwargs)

    return wrapper
