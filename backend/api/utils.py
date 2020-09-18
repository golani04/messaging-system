from functools import wraps
from typing import Optional

from flask_jwt_extended import current_user
from flask_sqlalchemy import DefaultMeta, Model

from . import errors


def check_item_exists(model: DefaultMeta) -> Optional[Model]:
    def outer_wrapper(f):
        @wraps(f)
        def inner_wrapper(id: int, *args, **kwargs):
            # current_user is of LocalProxy instance, it's how flask manage sessions
            # jwt extension possibly utilize this use so inorder to get to object behind it
            # I use method that provided by werkzeug library
            # https://werkzeug.palletsprojects.com/en/1.0.x/local/#werkzeug.local.LocalProxy._get_current_object
            if isinstance(current_user._get_current_object(), model) and current_user.id == id:
                # prevent unnecessary fetch of current user if ids mathches
                return f(current_user, *args, **kwargs)

            model_instance = model.find_by_id(id)

            if model_instance is None:
                return errors.not_found(
                    f"{model.__name__.title()} with this id: `{id}` is not exists."
                )

            return f(model_instance, *args, **kwargs)

        return inner_wrapper

    return outer_wrapper
