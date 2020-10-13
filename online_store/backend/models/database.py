"""This module provides database handle `db` and some useful related functions."""
import sqlite3
from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

db: SQLAlchemy = SQLAlchemy()


def get_db() -> sqlite3.Connection:
    """Get a database connection object for the current app."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):  # pylint: disable=invalid-name,W0613
    """Close the database connection to the app."""
    _db: sqlite3.Connection = g.pop('db', None)

    if _db is not None:
        _db.close()
