import os
import tempfile

import pytest

from loguru import logger
from pathlib import Path
from flask_jwt_extended import create_access_token

from online_store.app import create_app
from online_store.backend.models.database import db, get_db

try:
    with open(Path(__file__).parent / 'data.sql', 'rb') as f:
        _data_sql = f.read().decode('utf8')
except FileNotFoundError as err:
    logger.warning(err)
    _data_sql = ";"


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app(config={
        'TESTING': True,
        'DATABASE': db_path,
        'SQLALCHEMY_DATABASE_URI': f'sqlite:///{db_path}',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False
    })

    with app.app_context():
    #     init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def test_auth_headers(app):
    with app.app_context():
        access_token = create_access_token('test')
        headers = {
            'Authorization': 'Bearer {}'.format(access_token)
        }
        yield headers


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/auth/login',
            data={'username': username, 'password': password}
        )

    def logout(self):
        return self._client.get('/auth/logout')


@pytest.fixture
def auth(client):
    return AuthActions(client)
