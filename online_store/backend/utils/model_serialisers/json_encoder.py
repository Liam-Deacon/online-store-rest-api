"""This module defines a custom JSON encoder for sqlalchemy models."""
import json

from typing import Any, List
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    """Custom JSON encoder class for sqlalchemy ORM objects.

    Examples
    --------
    >>> json.dumps(obj, cls=AlchemyEncoder)

    Attributes
    ----------
    EXCLUDED_FIELDS: List[str]
        The names of fields to ignore when encoding object to JSON.
    """

    EXCLUDED_FIELDS: List[str] = ['metadata', 'query']

    def default(self, obj: Any) -> Any:  # pylint: disable=E0202,W0221
        """Custom JSON encoding method accounting for sqlalchemy ORM objects"""
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj)
                          if not x.startswith('_') and
                          x not in self.EXCLUDED_FIELDS and
                          not callable(getattr(obj, x))]:
                data = obj.__getattribute__(field)
                try:
                    # NOTE: json.dumps will still fail on non-encodable values
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
