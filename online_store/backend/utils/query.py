"""Provides useful utility functions when performing & returning ORM queries."""
import json
import sqlalchemy.exc

from functools import wraps
from http import HTTPStatus
from flask import request, Response
from loguru import logger

from .model_serialisers.json_encoder import AlchemyEncoder


def safe_query(func):
    """Decorator for ensuring a function returns a Response object.

    On occurance of an sqlalchemy.exc.InvalidRequestError, the error will
    be logged to the loguru.logger instance before a Response with 400
    BAD REQUEST code and a JSON body with an 'error' key-value pair
    containing the error message.

    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except sqlalchemy.exc.InvalidRequestError as err:
            logger.error(f'Error handling {request.url} due to: "{err}"')
            return Response({'error': str(err)}, mimetype='application/json',
                            status=HTTPStatus.BAD_REQUEST)
        except Exception as err:
            logger.error(f'Error handling {request.url} due to: "{err}"')
            return Response({'error': str(err)}, mimetype='application/json',
                            status=HTTPStatus.INTERNAL_SERVER_ERROR)
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
        if not data:
            code = HTTPStatus.NO_CONTENT  # No data
    except Exception as err:
        # NOTE: likely an issue with serialisation of obj with AlchemyEncoder
        logger.exception(err)
        logger.error(err)
        code = HTTPStatus.INTERNAL_SERVER_ERROR
    return Response(data, mimetype='application/json', status=code.value)
