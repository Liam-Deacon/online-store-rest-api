"""
Provides endpoints for user authentication using JSON web tokens.

Warnings
--------
The flask app must be configured to blacklist JWTs, e.g.

.. code-block:: python

    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

"""
from typing import Iterable
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity,
    jwt_refresh_token_required, get_raw_jwt
)
from loguru import logger
import sqlalchemy

from ..models.user import UserModel
from ..models.database import db


auth_router = Blueprint("auth", __name__, url_prefix="/auth")
blacklisted_tokens = set()


def check_request_json(
        needed_keys: Iterable[str] = ['username', 'password']) -> tuple:
    """Checks JSON in HTTP request and raises ValueError if needed_keys
    are missing.

    Parameters
    ----------
    needed_keys: List[str]
        A set of keys that must be included within JSON data.

    Returns
    -------
    tuple
        A tuple of the values given by `needed_keys`.

    Raises
    ------
    ValueError
        When reuqest is invalid or not all needed_keys are found in JSON data.

    """
    if not request.is_json:
        raise ValueError("Missing JSON in request")

    def raise_error_on_json_load_failed(e):
        raise ValueError(f'{e.__class__.__name__}: {e}')

    request.on_json_loading_failed = raise_error_on_json_load_failed

    data = request.get_json(force=True)
    for key in needed_keys:
        if key not in data:
            raise ValueError(f'Missing {key} parameter')

    return tuple((request.json.get(key) for key in needed_keys))


@auth_router.route('/login', methods=['POST'])
def login():
    """
    User authentication method.
    ---
    description: Authenticate user with supplied credentials.
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
      200:
        description: User successfully logged in.
      400:
        description: User login failed.
    tags:
        - authentication
    """
    try:
        username, password = check_request_json(['username', 'password'])
    except ValueError as err:
        return jsonify({'msg': str(err), 'status': 'error', 'code': 400}), 400

    user = UserModel.query.filter_by(username=username).first()
    if not user:
        return jsonify({'msg': 'Invalid username',
                        'status': 'error', 'code': 400}), 400
    elif not UserModel.verify_hash(password, user.password):
        return jsonify({'msg': 'Invalid password', 
                        'status': 'error', 'code': 400}), 400

    # Identity can be any data that is json serialisable
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token, status='ok', code=200), 200


@auth_router.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    """
    User authentication refresh method.
    ---
    description: Refresh authentication of user with supplied credentials.
    security:
      - bearerAuth: []
    parameters:
      - name: username
        in: formData
        type: string
        required: true
      - name: password
        in: formData
        type: string
        required: true
    responses:
      200:
        description: User successfully refreshed token.
      400:
        description: User authentication failed.
    tags:
        - authentication
    """
    current_user = get_jwt_identity()
    ret = {
        'access_token': create_access_token(identity=current_user),
        'status': 'ok',
        'code': 200
    }
    return jsonify(ret), 200


@auth_router.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    """
    User logout method.
    ---
    description: Revoke user authentication.
    security:
      - bearerAuth: []
    responses:
      200:
        description: User successfully logged out.
    tags:
        - authentication
    """
    jti = get_raw_jwt()['jti']
    blacklisted_tokens.add(jti)
    return jsonify({"msg": "Successfully logged out",
                    "status": "ok", "code": 200}), 200


@auth_router.route('/revoke', methods=['DELETE'])
@jwt_refresh_token_required
def revoke_refresh_token():
    """
    Revoke JWT refresh token.
    ---
    description: Revoke JWT refresh token.
    responses:
        200:
            description: Successfully revoked refresh token.
    tags:
        - authentication
    """
    jti = get_raw_jwt()['jti']
    blacklisted_tokens.add(jti)
    return jsonify({"msg": "Successfully revoked refresh token",
                    "status": "ok", "code": 200}), 200


@auth_router.route('/register', methods=['POST'])
def register():
    """
    User registration method.
    ---
    description: Register user with supplied credentials.
    security:
      - bearerAuth: []
    parameters:
      - in: body
        name: user
        description: The user to create.
        schema:
          type: object
          required:
            - username
            - password
            - email
          properties:
            username:
                type: string
            password:
                type: string
            email:
                type: string
            firstname:
                type: string
            lastname:
                type: string
            phone:
                type: string
            address:
                type: string
    examples:
        John Doe:
            username: john
            email: john.doe@fake.org
            password: janedoe
    responses:
      200:
        description: User successfully registered.
      400:
        description: Unable to register user.
    tags:
        - authentication
    """
    code = 200
    status = 'ok'
    msg = 'success'

    try:
        username, password, email = \
            check_request_json(['username', 'password', 'email'])
        query = UserModel.query.filter((UserModel.username == username) |
                                       (UserModel.email == email)).first()
        if query:
            field = 'username' if query.username == username else 'email'
            msg, status, code = f"{field} is not unique", 'error', 400
        else:
            try:
                user = UserModel(username=username, email=email,
                                 password=UserModel.generate_hash(password))
                db.session.add(user)
                db.session.commit()
            except sqlalchemy.exc.DBAPIError as err:
                db.session.rollback()
                logger.exception(err)
                msg, status, code = str(err), 'error', 400
    except ValueError as err:
        msg, status, code = str(err), "error", 400
    return jsonify(msg=msg, status=status, code=code), code


@auth_router.route('/remove', methods=['DELETE'])
@jwt_required
def remove_user():
    """
    User removal method.
    ---
    description: Remove the authenticated user from registered users.
    security:
      - bearerAuth: []
    responses:
      200:
        description: User successfully deleted.
      400:
        description: Unable to delete user.
    tags:
        - authentication
    """
    msg = "success"
    status = "ok"
    code = 200

    jti = get_raw_jwt()['jti']
    blacklisted_tokens.add(jti)
    username = get_jwt_identity()

    try:
        user = UserModel.query.filter_by(username=username).first()
        db.session.delete(user)
        db.session.commit()
    except sqlalchemy.exc.DBAPIError as err:
        db.session.rollback()
        logger.exception(err)
        msg, status, code = str(err), 'error', 400

    return jsonify(msg=msg, status=status, code=code), code
