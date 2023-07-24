import os.path

import pytest

from eyeflask import create_app


@pytest.fixture(scope="session")
def client():
    test_config = 'test_config.cfg'
    test_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    test_config)
    app = create_app(test_config_path)
    app.testing = True
    app.debug = True
    with app.test_client() as client:
        yield client
