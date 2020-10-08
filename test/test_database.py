import sqlite3

from flask import g
from online_store.db import get_db, close_db


def test_get_db(app):
    with app.app_context():
        db = get_db()
        assert hasattr(db, 'row_factory')
        assert db.row_factory == sqlite3.Row
        assert isinstance(db, sqlite3.Connection)


def test_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is not None
        close_db()
        assert not g.get('db', None)
        close_db()
