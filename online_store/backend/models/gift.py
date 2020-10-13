"""Defines models for gift list."""
from sqlalchemy import Column, Integer, ForeignKey
from .database import db


class GiftModel(db.Model):  # pylint: disable=too-few-public-methods
    """Model defining a gift.

    Attributes
    ----------
    id: int
        The unique ID of the gift item.
    item_id: int
        The unique ID of the store item from the items table.
    list_id: int
        The unique ID of the gift list from the gift_lists table.
    available: int
        The number of the gift that the couple desire,
        but have yet to be purchased.
    purchased: int
        The numbe rof the gift purchased.
    """
    __tablename__ = 'gifts'

    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    item_id = Column(ForeignKey('items.id'), nullable=False)
    list_id = Column(ForeignKey('gift_lists.id'), nullable=False)
    available = Column(Integer, default=1, nullable=False)
    purchased = Column(Integer, default=0, nullable=False)


class GiftListModel(db.Model):  # pylint: disable=too-few-public-methods
    """Model for gift list.

    Attributes
    ----------
    id: int
        The unique ID of the gift list within the gift_lists table.
    user_id: int
        The unique ID of the user who created the list from the users table.
    """
    __tablename__ = 'gift_lists'

    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    user_id = Column(ForeignKey('users.id'), nullable=True)  # allow anon
