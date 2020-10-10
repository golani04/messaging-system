import os
from datetime import timedelta

from dotenv import load_dotenv

# load env variables
load_dotenv()
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))


class Config:
    API_TITLE = "Messaging system"
    API_VERSION = "v1"
    OPENAPI_VERSION = "3.0.2"
    # OPENAPI_JSON_PATH = "api-spec.json"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_REDOC_PATH = "redoc"
    OPENAPI_REDOC_URL = "https://rebilly.github.io/ReDoc/releases/latest/redoc.min.js"
    OPENAPI_SWAGGER_UI_PATH = "swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = f"sqlite:////{project_path}/{os.getenv('DBNAME')}"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ERROR_MESSAGE_KEY = "errors"
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
