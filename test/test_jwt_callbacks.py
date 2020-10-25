
"""Provides custom callback functions for jsonfied responses to JWT access."""
import pytest
from http import HTTPStatus
from online_store.backend.utils.jwt_callbacks import *


def test_jsonified_claims_verification_callback():  # pylint: disable=invalid-name
    """Called when user claims is verified."""
    with pytest.raises(NotImplementedError):
        jsonified_claims_verification_callback()


def test_jsonified_claims_verification_failed_callback():  # pylint: disable=invalid-name,unused-argument
    """Called when the user claims verification callback returns False"""
    with pytest.raises(NotImplementedError):
        jsonified_claims_verification_failed_callback('token')


def jsonified_user_loader_error_callback():  # pylint: disable=invalid-name
    """Called when user loader error occurs."""
    with pytest.raises(NotImplementedError):
        jsonified_user_loader_error_callback()


def _test_response(data, msg, status='error', code=HTTPStatus.UNAUTHORIZED):
    assert isinstance(data, dict)
    assert "msg" in data.keys()
    assert data['msg'] == msg
    assert "status" in data.keys()
    assert data["status"] == "error"
    assert data["code"] == int(HTTPStatus.UNAUTHORIZED)


@pytest.mark.parametrize(
    ['func', 'msg'],
    [(jsonified_expired_token_callback, "Unauthorised: Access token has expired"),
     (jsonified_invalid_token_callback, "Unauthorised: Invalid access token"),
     (jsonified_needs_fresh_token_callback, "Unauthorised: Access token must be refreshed"),
     (jsonified_revoked_token_callback, "Unauthorised: Access token revoked"),
     (jsonified_token_in_blacklist_callback, "Unauthorised: Access token has been blacklisted"),
     (jsonified_unauthorized_callback, "Unauthorised: No access token in request header")]
)
def test_jsonified_callback_function(app, func, msg):
    with app.app_context():
        response, code = func('token')
        assert code == HTTPStatus.UNAUTHORIZED
        _test_response(response.get_json(force=True), msg)
