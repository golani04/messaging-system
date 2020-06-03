from flask import Flask
from .config import Config
from .database import DB


db = DB()


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # init packages
    db.init_app(app)
    # register blueprint
    # app should be instantiated before importing blueprint
    from backend.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    return app
