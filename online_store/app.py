"""This module defines the Flask app instance, created using `create_app()`."""
import os
import re

from collections import defaultdict
from pathlib import Path
from typing import Any, Mapping
from flask import Flask
from loguru import logger

# Flask middleware and extensions
from flask_jwt_extended import JWTManager
from flasgger import Swagger

# SQL and ORM
from .backend.models.database import db as store_db
from .backend.models.item import ItemModel  # TODO: refactor, not really needed

# route blueprints
from .backend.routes.auth import auth_router as backend_auth_router
from .backend.routes.gifts import gifts_router as backend_gifts_router
from .backend.routes.store import store_router as backend_store_router
from .backend.routes.terms_of_use import terms_of_user_router

__author__ = "Liam Deacon"
__description__ = "Wedding Gift List"


def load_config(app: Flask, config: Mapping[str, Any] = {}):
    """Loads the app config.

    The loading order is:

        1. config mapping
        2. os.environ
        3. conf file, with the path based off FLASK_CONFIG_DIR and FLASK_ENV

    This means that conf file variables have the highest priority and config mapping
    vairables have the lowest if there are duplicated keys.


    Parameters
    ----------
    app: Flask
        A flask app instance whose config we wish to update.
    config: Mapping[str, Any]
        A custom config (useful for testing purposes).

    """
    app.config.from_mapping(**config)
    logger.debug(f'Loaded Flask config from {config}')
    # logger.debug(f'User environment is: {os.environ}')

    def set_config(key: str, default: Any = None):
        """Set config from os.environ, falling back to config mapping."""
        key = key.upper()
        value = os.environ.get(key, config.get(key, default))
        if value is not None:
            app.config[key] = value

    set_config('FLASK_ENV', 'development')
    set_config('SQLALCHEMY_DATABASE_URI',
               'sqlite:///store.db')  # set default database
    set_config('JWT_SECRET_KEY', 'secret-squirrel')  # Change this!
    set_config('JWT_BLACKLIST_ENABLED', False)
    set_config('JWT_BLACKLIST_TOKEN_CHECKS', 'access,refresh')
    set_config('FLASK_APP_CONFIG_DIR', Path(__file__).parent)

    try:
        app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = \
            app.config['JWT_BLACKLIST_TOKEN_CHECKS'].split(',')
    except AttributeError:
        pass

    config_dir = Path(app.config['FLASK_APP_CONFIG_DIR'])
    logfile = f"{__description__.lower().replace(' ', '_')}.log"

    logfile_kwargs = defaultdict(
        lambda: {"rotation": "10MB", "compression": "zip", "backtrace": False},
        {"development": {"backtrace": True}}
    )

    environment = app.config['FLASK_ENV']
    config_file = config_dir / f'config/{environment}_env.cfg'
    if Path(environment).exists():
        config_file = environment

    try:
        logger.add(logfile, **logfile_kwargs[environment])
        app.config.from_pyfile(config_file)
        logger.info(f'Loaded Flask config from "{config_file}"')
    except IOError as err:
        logger.exception(err)

    # Note the flask app configuration setup
    logger.info(f'Running {environment} environment')
    logger.debug(f'App config is {app.config}')


def create_app(*args, **kwargs) -> Flask:
    """Function for creating the flask app instance.

    This app currently uses the following middleware/flask extensions:

        - JWTManager (flask-jwt-extended) for JSON web token authentication.
        - Swagger (flasgger) for interactively viewing the REST API
          under `/apidocs`.

    .. todo::

        This function is too complex, performing many changes
        (for instance uses user env and conf files together)
        and therefore needs refactoring in order to be more easily
        (and thoroughly) tested.

    """
    config = kwargs.pop('config', {})
    app = Flask(__name__, *args, **kwargs)
    load_config(app, config or {})

    # Apply JWT authentication middleware
    jwt = JWTManager(app)  # TODO: use jwt

    # Add Swagger apidocs
    Swagger(app,
            template={
                "info": {
                    "title": f"Example {__description__} REST API by {__author__}",
                    "version": "0.0.1",
                    "openapi": "3.0.3",
                    "termsOfService": "/terms"
                },
                'uiversion': "2",
                "components": {
                    "securitySchemes": {
                        "bearer": {
                            "type": "http",
                            "scheme": "bearer"
                        },
                        "bearerAuth": {
                            "type": "http",
                            "scheme": "bearer",
                            "bearerFormat": "JWT",
                            "in": "header",
                        }
                    }
                },
                'security': [{'bearerAuth': []}],
                'securityDefinitions': {
                    'basicAuth': {'type': 'basic'},
                    'bearerAuth': {
                        'type': 'apiKey',
                        'name': 'Authorization',
                        'in': 'header'
                    }
                }
            })

    # Create database resources.
    store_db.init_app(app)
    with app.app_context():
        store_db.create_all()

        # try to load products if table is empty
        if len(ItemModel.query.all()) == 0:
            product_json_path = Path(__file__).parent.parent / 'products.json'
            logger.info(f'Loading JSON data from {product_json_path}')
            ItemModel.load_json(product_json_path)

    # # Register blueprint routes.
    app.register_blueprint(backend_store_router, url_prefix="/api/v1/store")
    app.register_blueprint(backend_auth_router, url_prefix="/api/v1/auth")
    app.register_blueprint(backend_gifts_router, url_prefix="/api/v1/gifts")
    app.register_blueprint(terms_of_user_router, url_prefix="")

    return app
