from typing import Type
import pytest
import json

from online_store.backend.utils.model_serialisers import json_encoder
from online_store.backend.models.database import db


class TestModel(db.Model):
    __tablename__ = 'test_model'

    a = db.Column(db.Integer(), primary_key=True)
    b = db.Column(db.Float(), nullable=True)
    _c = db.Column(db.Text())

    d: dict = {'goodbye!': 'cruel world'}
    o: object = None

    def test_method(self):
        return self.a + (self.b or 0)


@pytest.mark.parametrize(
    ('a', 'b', '_c', 'o', 'exception'),
    [(1, 2.0, 'hello', None, None),
     (1, None, 'hello', None, None),
     (None, 1.0, 'hello', None, TypeError),
     (1, 1.0, 'hello', pytest, None)]
)
def test_AlchemyEncoder(a, b, _c, o, exception):
    try:
        model = TestModel(a=a, b=b, _c=_c)
        TestModel.o = o
        data = json.loads(json.dumps(model, cls=json_encoder.AlchemyEncoder))
        for key in ('a', 'b', 'd'):
            assert key in data
            assert data[key] == getattr(model, key)
        for key in ('_c', 'metadata', 'query', 'test_method'):
            assert key not in data
        assert 'o' in data
        if o:  # FIXME: assuming o is either None or not encodable
            assert data['o'] is None
    except AssertionError:
        raise
    except Exception as err:
        assert isinstance(err, exception)


@pytest.mark.parametrize(
    ('obj', 'expected', 'exception'),
    [({}, {}, None),
     (object, None, TypeError)]
)
def test_AlchemyEncoder_fallback(obj, expected, exception):
    try:
        data = json.loads(json.dumps(obj, cls=json_encoder.AlchemyEncoder))
        assert data == expected
    except AssertionError:
        raise
    except Exception as err:
        assert isinstance(err, exception)
