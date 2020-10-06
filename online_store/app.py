import os
import re

from collections import defaultdict
from pathlib import Path
from flask import Flask, jsonify
from loguru import logger

from flask_jwt_extended import JWTManager
from flasgger import Swagger

from .backend.models.database import db as store_db
from .backend.models.item import ItemModel
from .backend.routes.auth import auth_router as backend_auth_router
from .backend.routes.gifts import gifts_router as backend_gifts_router
from .backend.routes.store import store_router as backend_store_router
from .backend.routes.terms_of_use import terms_of_user_router

__author__ = "Liam Deacon"
__description__ = "Wedding Gift List"


def create_app() -> Flask:
    app = Flask(__name__)

    # load config
    app.config['SQLALCHEMY_DATABASE_URI'] = \
        os.environ.get('SQLALCHEMY_DATABASE_URI',
                       'sqlite:///store.db')  # set default database
    app.config['JWT_SECRET_KEY'] = \
        os.environ.get('JWT_SECRET_KEY', 'secret-squirrel')  # Change this!

    app.config['JWT_BLACKLIST_ENABLED'] = False
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

    config_dir = Path(os.environ.get('FLASK_APP_CONFIG_DIR',
                                     Path(__file__).parent))

    logfile = f"{__description__.lower().replace(' ', '_')}.log"
    logfile_kwargs = defaultdict(
        lambda: {"rotation": "10MB", "compression": "zip", "backtrace": False},
        {"development": {"backtrace": True}}
    )

    environment = os.environ.get('FLASK_ENV', 'development')
    config_file = config_dir / f'config/{environment}_env.cfg'
    if Path(environment).exists():
        config_file = environment

    try:
        logger.add(logfile, **logfile_kwargs[environment])
        app.config.from_pyfile(config_file)
    except IOError as err:
        logger.exception(err)

    logger.info(f'Running {environment} environment')
    logger.debug(f'App config is {app.config}')

    # Apply JWT authentication middleware
    jwt = JWTManager(app)  # TODO: use jwt

    # Add Swagger apidocs
    Swagger(app,
            # config={
            #     'headers': [

            #     ],
            #     'specs': [
            #         {
            #             'endpoint': 'apispec',
            #             'route': '/apispec1.json'
            #         }
            #     ],
            # },
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
