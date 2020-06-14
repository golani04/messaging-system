from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .config import Config


db = SQLAlchemy()
jwt = JWTManager()


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # init packages
    db.init_app(app)
    jwt.init_app(app)
    # register blueprint
    # app should be instantiated before importing blueprint
    from backend.api import bp as api_bp
    from backend.auth import bp as auth_bp

    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app
