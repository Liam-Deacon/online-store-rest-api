import pytest

from flask import Response, jsonify
from http import HTTPStatus
from functools import partial
from sqlalchemy.exc import InvalidRequestError
from online_store.backend.utils.query import query_to_json_response, safe_query


@pytest.mark.parametrize(
    ['input_data', 'json_data', 'code'],
    [([], [], HTTPStatus.NO_CONTENT),
     ({}, {}, HTTPStatus.NO_CONTENT),
     (None, None, HTTPStatus.NO_CONTENT),
     (pytest, None, HTTPStatus.INTERNAL_SERVER_ERROR),
     ({'a': 1, 'b': 2.0}, {'a': 1, 'b': 2.0}, HTTPStatus.OK)]
)
def test_query_to_json_response(app, input_data, json_data, code):
    with app.app_context():
        response = query_to_json_response(input_data)
        assert isinstance(response, Response)
        if code != HTTPStatus.INTERNAL_SERVER_ERROR:
            assert response.get_json() == json_data
        assert int(code) == response.status_code


def _can_raise_exception(exc_cls, msg="Error occurred", *args, **kwargs):
    if exc_cls:
        raise exc_cls(msg)
    return jsonify({'msg': msg, 'status': 'ok', 'code': 200}), HTTPStatus.OK


@pytest.mark.parametrize(
    ['func', 'code'],
    [(partial(_can_raise_exception, exc_cls=InvalidRequestError), HTTPStatus.BAD_REQUEST),
     (partial(_can_raise_exception, exc_cls=ValueError), HTTPStatus.INTERNAL_SERVER_ERROR),
     (partial(_can_raise_exception, exc_cls=None, msg="success!"), HTTPStatus.OK)]
)
def test_safe_query(app, func, code):
    with app.test_request_context():
        wrapped_func = safe_query(func)
        response = wrapped_func()
        assert isinstance(response, tuple)
        assert len(response) == 2
        assert isinstance(response[0], Response)
        assert isinstance(response[1], HTTPStatus)
        # TODO: check status code from response
        assert int(response[0].status_code) == int(code), f'HTTP status should be {code}'
        assert response[1] == code

        body = response[0].get_json(silent=True)
        assert body
        assert 'msg' in body
        assert 'code' in body
        assert 'status' in body
        assert body['msg'] == 'Error occurred' \
            if int(code) != 200 else body['msg'] != "Error occured"
        assert body['code'] == int(code)
        assert body['status'] == 'ok' if int(code) == 200 else 'error'
