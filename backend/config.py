import os
from datetime import timedelta

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
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=15)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    JWT_TOKEN_LOCATION = ["cookies"]
    JWT_COOKIE_SECURE = True
    JWT_ACCESS_COOKIE_PATH = "/api"
    JWT_REFRESH_COOKIE_PATH = "/auth/refresh"
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_CSRF_IN_COOKIES = False


class DevConfig(Config):
    TEMPLATES_AUTO_RELOAD = True


if os.getenv("FLASK_ENV") == "development":
    Config = DevConfig
