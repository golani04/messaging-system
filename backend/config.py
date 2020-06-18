import os
from dotenv import load_dotenv


# load env variables
load_dotenv()
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{project_path}/{os.environ.get('DBNAME')}"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ERROR_MESSAGE_KEY = "messages"


class DevConfig(Config):
    TEMPLATES_AUTO_RELOAD = True


if os.environ.get("FLASK_ENV") == "development":
    Config = DevConfig
