"""This module defines the ORM models for store orders."""
from enum import Enum, auto
from sqlalchemy.sql import func
from sqlalchemy import Column, Integer, DateTime, ForeignKey
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


class OrderModel(db.Model):  # pylint: disable=too-few-public-methods
    """An ORM model class for defining each order."""
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    user = Column(Integer, nullable=False)
    created = Column(DateTime, default=func.now())
    last_updated = Column(DateTime, default=func.now())
    status = Column(Integer, default=int(OrderStatus.CREATED))


class OrderItemModel(db.Model):  # pylint: disable=too-few-public-methods
    """ORM model for defining each order item belonging to a given order."""
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)  # pylint: disable=invalid-name
    order_id = Column(Integer, ForeignKey('orders.id'))
    item = Column(Integer, ForeignKey('items.id'))
    quantity = Column(Integer)


class StockUnavailableError(Exception):  # pylint: disable=too-few-public-methods
    """An exception class for indicating there is no stock availability."""
    pass  # pylint: disable=unnecessary-pass
