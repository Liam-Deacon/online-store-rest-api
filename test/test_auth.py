import pytest
import json

from flask import g, session
from http import HTTPStatus
from online_store.db import get_db


def test_register_successful(client, app):
    response = client.post(
        '/api/v1/auth/register',
        data=json.dumps({'username': 'a', 'password': 'a', 'email': 'a@a.a'}),
        content_type='application/json'
    )
    # assert 'http://localhost/api/v1/auth/login' == response.headers['Location']
    assert response.status_code == 200

    with app.app_context():
        assert get_db().execute(
            "select * from users where username = 'a'",
        ).fetchone() is not None


def test_register_user_data_not_unique(client, app):
    response = client.post(
        '/api/v1/auth/register',
        data=json.dumps({'username': 'a', 'password': 'a', 'email': 'a@a.a'}),
        content_type='application/json'
    )
    # assert 'http://localhost/api/v1/auth/login' == response.headers['Location']
    assert response.status_code == 200

    with app.app_context():
        assert get_db().execute(
            "select * from users where username = 'a'",
        ).fetchone() is not None

    response = client.post(
        '/api/v1/auth/register',
        data=json.dumps({'username': 'a', 'password': 'a', 'email': 'a@a.a'}),
        content_type='application/json'
    )
    assert response.status_code == 400

    # check for uniqueness of username
    data = json.loads(response.get_data().decode())
    assert 'msg' in data
    assert data['msg'] == 'username is not unique'
    assert 'code' in data
    assert data['code'] == 400
    assert 'status' in data
    assert data['status'] == 'error'

    # check for uniqueness of email address
    response = client.post(
        '/api/v1/auth/register',
        data=json.dumps({'username': 'b', 'password': 'a', 'email': 'a@a.a'}),
        content_type='application/json'
    )
    assert response.status_code == 400

    data = json.loads(response.get_data().decode())
    assert 'msg' in data
    assert data['msg'] == 'email is not unique'
    assert 'code' in data
    assert data['code'] == 400
    assert 'status' in data
    assert data['status'] == 'error'


@pytest.mark.parametrize(
    ('username', 'password', 'email', 'message', 'code'), (
        ('', '', '', 'Missing username parameter', 400),
        (None, '', '', 'Missing username parameter', 400),
        ('a', '', '', 'Missing password parameter', 400),
        ('a', None, '', 'Missing password parameter', 400),
        ('b', 'b', '', 'Missing email parameter', 400),
        ('b', 'b', None, 'Missing email parameter', 400),
        ('b', 'b', 'b@b.com', 'Registration successful', 200),
        ('test', 'b', 'c@c.com', 'username is not unique', 400),
        ('c', 'c', 'test@test.com', 'email is not unique', 400)
    )
)
def test_register_validate_input(client, username, password,
                                 email, message, code):
    payload = {}

    # selectively add keys that are set
    if username is not None:
        payload['username'] = username
    if password is not None:
        payload['password'] = password
    if email is not None:
        payload['email'] = email

    response = client.post(
        '/api/v1/auth/register',
        data=json.dumps(payload),
        content_type='application/json'
    )
    data = json.loads(response.get_data().decode())
    assert 'msg' in data
    assert message == data['msg']
    assert 'code' in data
    assert code == data['code']
    assert 'status' in data
    assert data['status'] == ('error' if code != 200 else 'ok')
    assert code == response.status_code


@pytest.mark.skip(reason="TODO")
def test_login_successful():
    raise NotImplementedError


@pytest.mark.skip(reason="TODO")
def test_login_failure():
    raise NotImplementedError


@pytest.mark.parametrize(
    ('method', 'code'),
    [('POST', 405),
     ('GET', 405),
     ('DELETE', 200)]
)
def test_logout_successful(client, test_auth_headers, method, code):
    request = getattr(client, method.lower())
    response = request('/api/v1/auth/logout', headers=test_auth_headers)
    assert response.status_code == code
    if code == 200:
        data = json.loads(response.get_data().decode())
        assert 'msg' in data
        assert data['msg'] == 'Successfully logged out'
        assert 'status' in data
        assert data['status'] == 'ok'
        assert 'code' in data
        assert data['code'] == 200


def test_logout_no_token(client, app):
    response = client.delete('/api/v1/auth/logout')
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    data = json.loads(response.get_data().decode())
    assert 'msg' in data
    assert data['msg'] == 'Unauthorised: No access token in quest header'
    assert 'status' in data
    assert data['status'] == 'error'
    assert 'code' in data
    assert data['code'] == HTTPStatus.UNAUTHORIZED
