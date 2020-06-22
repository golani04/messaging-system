import os
import pytest
from backend import create_app, db
from backend.config import Config, project_path


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite://"


def default_data():
    with open(os.path.join(project_path, "tables.sql")) as f:
        sql = f.read()

    return sql


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.test_client() as client:
        # create demo db in memory
        with app.app_context():
            conn = db.engine.raw_connection()
            cursor = conn.cursor()
            cursor.executescript(default_data())

            yield client

            db.drop_all()
