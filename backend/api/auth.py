from backend import jwt
from backend.models.users import User


@jwt.user_loader_callback_loader
def load_user(identity):
    # set current user
    return User.query.get(identity)
