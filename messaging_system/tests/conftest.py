import os
import pytest
from backend import create_app, db as mainDB
from backend.config import Config, project_path


class TestConfig(Config):
    DATABASE_URL = ":memory:"


def get_init_data():
    with open(os.path.join(project_path, "tables.sql")) as f:
        sql = f.read()

    return sql


@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.test_client() as client:
        # create demo db in memory
        mainDB.cursor.executescript(get_init_data())
        yield client

    mainDB.conn.close()
