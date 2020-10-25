"""Provides useful utility functions when performing & returning ORM queries"""
import json

from typing import Tuple
from functools import wraps, partial
from http import HTTPStatus

from flask import request, jsonify, Response
from loguru import logger

import sqlalchemy.exc

from .model_serialisers.json_encoder import AlchemyEncoder


def JsonReponseTuple(data, **kwargs) -> Tuple[Response, HTTPStatus]:
    """Helper function for creating a json response tuple."""
    if isinstance(data, str):
        data_str, data = data, json.loads(data)
    else:
        data_str = json.dumps(data, cls=AlchemyEncoder)
    kwargs['status'] = kwargs.get('status', data.get('code', 200))
    kwargs['mimetype'] = 'application/json'
    response = Response(data_str, **kwargs), HTTPStatus(kwargs['status'])
    return response


def safe_query(func) -> Tuple[Response, HTTPStatus]:
    """Decorator for ensuring a function returns a response object.

    On occurance of an sqlalchemy.exc.InvalidRequestError, the error will
    be logged to the loguru.logger instance before a Response with 400
    BAD REQUEST code and a JSON body with an 'error' key-value pair
    containing the error message.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        json_response = partial(Response, mimetype='application/json')
        try:
            result = func(*args, **kwargs)
            # ensure result is a tuple of Response, HTTPStatus
            result = (result, HTTPStatus(result.status_code)) if isinstance(result, Response) else result
        except sqlalchemy.exc.InvalidRequestError as err:
            logger.error(f'Error handling {request.url} due to: "{err}"')
            result = JsonReponseTuple({'msg': str(err), 'status': 'error',
                                       'code': int(HTTPStatus.BAD_REQUEST)})
        except Exception as err:  # pylint: disable=broad-except
            # Catch any error not accounted for above
            logger.error(f'Error handling {request.url} due to: "{err}"')
            result = JsonReponseTuple({'msg': str(err), 'status': 'error',
                                       'code': int(HTTPStatus.INTERNAL_SERVER_ERROR)})
        return result
    return wrapper


def query_to_json_response(obj: object) -> Response:
    """Serialises obj (including ORM instances) & returns a JSON response.

    Returns
    -------
    Response
        A Response instance containing a JSON body and a status code.

    Notes
    -----
        The status code returned will be either:
            - 200 (OK) when serialised to json data successfully.
            - 204 (NO CONTENT) when data is empty.
            - 500 (INTERNAL SERVER ERROR) when an exception occurs.

    """
    data = []
    code = HTTPStatus.OK
    try:
        data = json.dumps(obj, cls=AlchemyEncoder)
        if not data or data in (r'{}', '[]', 'null'):
            code = HTTPStatus.NO_CONTENT  # No data
    except Exception as err:  # pylint: disable=broad-except
        # NOTE: likely an issue with serialisation of obj with AlchemyEncoder
        logger.exception(err)
        logger.error(err)
        code = HTTPStatus.INTERNAL_SERVER_ERROR
    return Response(str(data), mimetype='application/json', status=code.value)
