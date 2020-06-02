import pytest
from backend import create_app


@pytest.fixture
def app():
    app = create_app()

    with app.test_client() as client:
        yield client
