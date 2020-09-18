# base on this article https://www.michaelcho.me/article/using-python-enums-in-sqlalchemy-models
from sqlalchemy import Integer

from backend import db


class SQLAIntEnum(db.TypeDecorator):
    """Swap integer with enum when model is parsed or vice versa"""

    impl = Integer

    def __init__(self, enumtype, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._enumtype = enumtype

    def proccess_bind_param(self, value, dialect):
        if isinstance(value, int):
            return value

        return value.value

    def process_result_value(self, value, dialect):
        return self._enumtype(value)
