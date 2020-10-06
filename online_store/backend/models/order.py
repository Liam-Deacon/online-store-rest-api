from enum import Enum, auto
from http.client import PAYMENT_REQUIRED
from sqlalchemy.sql import func

from .database import db


class OrderStatus(Enum):
    """Enumeration representing different states for each Order

    Attributes
    ----------
    INVALID: int
        Indicates there was a problem creating the order and no record
        added to the list of orders.
    CREATED: int
        Indicates the order has been created, but the purchase is yet to be
        confirmed.
    PAYMENT_RECEIVED: int
        Indicates the order has been confirmed, but the purchase is yet to be
        shipped.
    SHIPPED: int
        Indicates order has been shipped, but not yet delivered to customer.
    DELIVERED: int
        Indicates the order has been delivered to the customer.
    REFUNDED: int
        Indicates the order has been refunded.
    VOIDED: int
        Indicates the order has been cancelled.

    """
    INVALID: int = -1
    CREATED: int = auto()
    PAYMENT_RECEIVED: int = auto()
    SHIPPED: int = auto()
    DELIVERED: int = auto()
    REFUNDED: int = auto()
    VOIDED: int = auto()

    def __int__(self) -> int:
        """Convenience shorthand integer representation of enum"""
        return self.value

    def __str__(self) -> str:
        """Convenience shorthand string representation of enum (for humans)"""
        return self.name


class OrderModel(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=func.now())
    last_updated = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.Integer, default=int(OrderStatus.CREATED))


class OrderItemModel(db.Model):
    __tablename__ = "order_items"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'))
    item = db.Column(db.Integer, db.ForeignKey('items.id'))
    quantity = db.Column(db.Integer)


class StockUnavailableError(Exception):
    pass
