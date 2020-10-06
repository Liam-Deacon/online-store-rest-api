"""Defines models for gift list."""
from .database import db


class GiftModel(db.Model):
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

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.ForeignKey('items.id'), nullable=False)
    list_id = db.Column(db.ForeignKey('gift_lists.id'), nullable=False)
    available = db.Column(db.Integer, default=1)
    purchased = db.Column(db.Integer, default=0)


class GiftListModel(db.Model):
    """Model for gift list.

    Attributes
    ----------
    id: int
        The unique ID of the gift list within the gift_lists table.
    user_id: int
        The unique ID of the user who created the list from the users table.
    """
    __tablename__ = 'gift_lists'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.ForeignKey('users.id'), nullable=True)  # allow anon
