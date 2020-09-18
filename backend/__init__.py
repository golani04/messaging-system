from datetime import datetime
from sqlite3 import Connection as SQLiteConnection

from flask import Flask, json
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from secure import SecureCookie, SecureHeaders
from sqlalchemy import event
from sqlalchemy.engine import Engine

from backend.config import Config
from backend.const import DATETIME_FORMAT

db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()
secure_cookie = SecureCookie()
secure_headers = SecureHeaders()


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime(DATETIME_FORMAT)

        return json.JSONEncoder.default(self, obj)


# TODO: consider to use flask_smorest, to use redoc and OpenAPI
#       https://flask-smorest.readthedocs.io/en/latest
def create_app(config_obj=Config):
    Flask.json_encoder = CustomJSONEncoder
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # init packages
    db.init_app(app)
    jwt.init_app(app)
    ma.init_app(app)
    # register blueprint
    # app should be instantiated before importing blueprint
    from backend.api import bp as api_bp
    from backend.auth import bp as auth_bp
    from backend.errors import bp as errors_bp

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(errors_bp)

    return app


# init foreign keys in sqlite database
@event.listens_for(Engine, "connect")
def turn_on_foreign_keys(dbapi_conn, *args):
    if isinstance(dbapi_conn, SQLiteConnection):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys = 1;")
        cursor.close()
