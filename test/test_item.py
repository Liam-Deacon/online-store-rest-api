import json
import pytest

from tempfile import TemporaryFile
from online_store.db import get_db
from online_store.backend.models.item import ItemModel, ItemImageModel

DUMMY_ITEMS = [
    {'id': '400', 'name': 'My test product', 'brand': 'stuff', 'price': '28.11GBP', 'in_stock_quantity': 10}
]


@pytest.mark.skip('FIXME: cannot use json.dump on temp file')
def test_ItemModel_load_json(app):
    with app.app_context():
        db_conn = get_db()
        assert db_conn.execute(
            "SELECT * FROM users WHERE id>300",
        ).fetchone() is None

        with TemporaryFile('wb+') as temp_fp:
            json.dump(DUMMY_ITEMS, temp_fp)
            temp_fp.seek(0)
            ItemModel.load_json(temp_fp)

        result = db_conn.execute("SELECT * FROM users WHERE id>300").fetchone()
        assert result is not None


def test_ItemImageModel_default_image():
    image = ItemImageModel.default_image()
    assert isinstance(image, str)
    assert image.startswith('data:image/svg+xml;base64,')
