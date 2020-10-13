import http
import pytest

from flask import Response
from http import HTTPStatus
from online_store.backend.utils.query import query_to_json_response


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
