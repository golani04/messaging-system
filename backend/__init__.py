from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlite3 import Connection as SQLiteConnection

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

from .config import Config


db = SQLAlchemy()
jwt = JWTManager()
ma = Marshmallow()


def create_app(config_obj=Config):
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

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app


# init foreign keys in sqlite database
@event.listens_for(Engine, "connect")
def turn_on_foreign_keys(dbapi_conn, *args):
    if isinstance(dbapi_conn, SQLiteConnection):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys = 1;")
        cursor.close()
