"""This module provides a class for describing store items as an ORM model."""
from typing import Union
from pathlib import Path

import re
import json

from loguru import logger
from sqlalchemy import Column, Integer, Float, ForeignKey, Text

import sqlalchemy.exc


from .database import db


class ItemModel(db.Model):  # pylint: disable=too-few-public-methods
    """Model representing a store item.

    Attributes
    ----------
    id: int
        The unique ID of the item in the store within the items table.
    name: str
        User friendly name describing the item.
    brand: str
        The manufacturer of the item.
    price: float
        The amount charged for the item.
    currency: str
        The currency that the item will be charged in when purchasing.
    in_stock_quantity: int
        The number of the item in stock.
    """
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    name = Column(Text)
    brand = Column(Text)  # TODO: add brands table & change to ForeignKey
    price = Column(Float, nullable=True)
    currency = Column(Text)  # TODO: change to foreign key for currencies
    in_stock_quantity = Column(Integer, nullable=False)

    @classmethod
    def load_json(cls, filepath: Union[Path, str]):
        """Convenience method for loading JSON data into items table."""
        with open(filepath) as json_fp:
            data = json.load(json_fp)

            for i, item in enumerate(data):
                logger.info(f"Loading store item {i} into database")
                price = item.get('price', None)
                if isinstance(price, str):
                    item['price'] = float(re.sub('[A-Za-z ]+', '', price))
                    item['currency'] = re.sub('[0-9,\\.]+', '', price)
                try:
                    db.session.add(cls(**item))
                    db.session.commit()
                except sqlalchemy.exc.IntegrityError as err:
                    logger.error(err)
                    db.session.rollback()


class ItemImageModel(db.Model):  # pylint: disable=too-few-public-methods
    """Defines a table for displaying items to the user.

    Notes
    -----
    This is a separate table from the `items` table so as to improve
    performance, especially as base64 encoded image data may be large.
    """
    __tablename__ = 'item_images'

    id = Column(ForeignKey('items.id'), primary_key=True)  # pylint: disable=invalid-name
    base64_image = Column(Text, nullable=True)

    @classmethod
    def default_image(cls) -> str:
        """Return a default base64 encoded image."""
        return "data:image/svg+xml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0iaXNvLTg4NTktMSI/Pg0KPCEtLSBHZW5lcmF0b3I6IEFkb2JlIElsbHVzdHJhdG9yIDE2LjAuMCwgU1ZHIEV4cG9ydCBQbHVnLUluIC4gU1ZHIFZlcnNpb246IDYuMDAgQnVpbGQgMCkgIC0tPg0KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4NCjxzdmcgdmVyc2lvbj0iMS4xIiBpZD0iQ2FwYV8xIiB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHhtbG5zOnhsaW5rPSJodHRwOi8vd3d3LnczLm9yZy8xOTk5L3hsaW5rIiB4PSIwcHgiIHk9IjBweCINCgkgd2lkdGg9IjMxLjM1N3B4IiBoZWlnaHQ9IjMxLjM1N3B4IiB2aWV3Qm94PSIwIDAgMzEuMzU3IDMxLjM1NyIgc3R5bGU9ImVuYWJsZS1iYWNrZ3JvdW5kOm5ldyAwIDAgMzEuMzU3IDMxLjM1NzsiDQoJIHhtbDpzcGFjZT0icHJlc2VydmUiPg0KPGc+DQoJPHBhdGggZD0iTTE1LjI1NSwwYzUuNDI0LDAsMTAuNzY0LDIuNDk4LDEwLjc2NCw4LjQ3M2MwLDUuNTEtNi4zMTQsNy42MjktNy42Nyw5LjYyYy0xLjAxOCwxLjQ4MS0wLjY3OCwzLjU2Mi0zLjQ3NSwzLjU2Mg0KCQljLTEuODIyLDAtMi43MTItMS40ODItMi43MTItMi44MzhjMC01LjA0Niw3LjQxNC02LjE4OCw3LjQxNC0xMC4zNDNjMC0yLjI4Ny0xLjUyMi0zLjY0My00LjA2Ni0zLjY0Mw0KCQljLTUuNDI0LDAtMy4zMDYsNS41OTItNy40MTQsNS41OTJjLTEuNDgzLDAtMi43NTYtMC44OS0yLjc1Ni0yLjU4NEM1LjMzOSwzLjY4MywxMC4wODQsMCwxNS4yNTUsMHogTTE1LjA0NCwyNC40MDYNCgkJYzEuOTA0LDAsMy40NzUsMS41NjYsMy40NzUsMy40NzZjMCwxLjkxLTEuNTY4LDMuNDc2LTMuNDc1LDMuNDc2Yy0xLjkwNywwLTMuNDc2LTEuNTY0LTMuNDc2LTMuNDc2DQoJCUMxMS41NjgsMjUuOTczLDEzLjEzNywyNC40MDYsMTUuMDQ0LDI0LjQwNnoiLz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjxnPg0KPC9nPg0KPGc+DQo8L2c+DQo8Zz4NCjwvZz4NCjwvc3ZnPg0K"  # pylint: disable=C0301; noqa
