"""Provides custom callback functions for jsonfied responses to JWT access."""
from http import HTTPStatus
from flask import jsonify


def jsonified_claims_verification_callback():
    raise NotImplementedError


def jsonified_claims_verification_failed_callback(token):
    """Called when the user claims verification callback returns False"""
    raise NotImplementedError


def jsonified_expired_token_callback(token):
    """Called when an expired token accesses a protected endpoint"""
    return jsonify({
        "msg": "Unauthorised: Access token has expired",
        "status": "error",
        "code": HTTPStatus.UNAUTHORIZED
    }), HTTPStatus.UNAUTHORIZED


def jsonified_invalid_token_callback(token):
    """Called when an invalid token accesses a protected endpoint"""
    return jsonify({
        "msg": "Unauthorised: Invalid access token",
        "status": "error",
        "code": HTTPStatus.UNAUTHORIZED
    }), HTTPStatus.UNAUTHORIZED


def jsonified_needs_fresh_token_callback(token):
    """Called when a non-fresh token accesses a fresh_jwt_required() endpoint"""
    return jsonify({
        "msg": "Unauthorised: Access token must be refreshed",
        "status": "error",
        "code": HTTPStatus.UNAUTHORIZED
    })


def jsonified_revoked_token_callback(token):
    """Called when a revoked token accesses a protected endpoint."""
    return jsonify({
        "msg": "Unauthorised: Access token revoked",
        "status": "error",
        "code": HTTPStatus.UNAUTHORIZED
    }), HTTPStatus.UNAUTHORIZED


def jsonified_token_in_blacklist_callback(token):
    """Called to check if a token has been revoked."""
    return jsonify({
        "msg": "Unauthorised: Access token has been blacklisted",
        "status": "error",
        "code": HTTPStatus.UNAUTHORIZED
    }), HTTPStatus.UNAUTHORIZED


def jsonified_unauthorized_callback(token):
    """Called when a request with no JWT accesses a protected endpoint."""
    return jsonify({
        "msg": "Unauthorised: No access token in request header",
        "status": "error",
        "code": HTTPStatus.UNAUTHORIZED
    }), HTTPStatus.UNAUTHORIZED


def jsonified_user_loader_error_callback():
    raise NotImplementedError
