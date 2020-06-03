from flask import Flask
from .config import Config
from .database import DB


db = DB()


def create_app(config_obj=Config):
    app = Flask(__name__)
    app.config.from_object(config_obj)
    db.init_app(app)

    return app
