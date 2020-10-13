"""Module for providing store API routes."""
from typing import List, Optional, Union
from http import HTTPStatus

from sqlalchemy.orm import load_only
import sqlalchemy.exc

from flask import Blueprint, request, Response
from loguru import logger

from ..models.database import db
from ..models.item import ItemModel
from ..models.user import UserModel
from ..models.order import (
    OrderItemModel, OrderModel, OrderStatus, StockUnavailableError
)
from ..utils.query import safe_query, query_to_json_response

store_router = Blueprint('store', __name__, url_prefix='/store')  # pylint: disable=invalid-name


@store_router.route('/')
def store():
    """Return the default route for the store."""
    return Response(None, mimetype='application/json',
                    status=HTTPStatus.NOT_IMPLEMENTED)


@store_router.route('/items', strict_slashes=False)
@safe_query
def items():
    """
    List items method.
    ---
    description: Retrieve list of items in store.
    responses:
      200:
        description: List of items.
      400:
        description: Unable to handle request.
    tags:
        - store
    """
    params = dict(request.args)
    fields: Optional[List[str]] = \
        str(params.pop('fields', "")).split(',')
    purchased: bool = bool(params.pop('purchased', False))  # pylint: disable=unused-variable
    query = ItemModel.query \
                     .filter_by(**params) \
                     .options(load_only(*fields))  # FIXME:
    return query_to_json_response(query.all())


@store_router.route('/items', methods=['POST'])
def create_item():
    """
    Create a new item.
    ---
    description: Add a new item to the store.
    responses:
      200:
        description: Item was successfully added.
      400:
        description: Unable to create item.
    tags:
        - store
    """
    raise NotImplementedError


@store_router.route('/items/id/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    """
    Delete item from store. [Requires admin user]
    ---
    tags:
      - store
    """
    raise NotImplementedError


@store_router.route('/items/id/<int:item_id>', strict_slashes=False)
def item(item_id: int):
    """
    Single item data retrieval method.
    ---
    description: Retrieve individual item data.
    parameters:
      - in: path
        name: item_id
        type: integer
        required: true
        description: The unique integer ID representing a store item.
    responses:
      200:
        description: Items details.
      400:
        description: Unable to handle request.
    tags:
        - store
    """
    query = ItemModel.query.filter_by(id=item_id)
    return query_to_json_response(query.first())


def _create_order(order_data: dict) -> OrderStatus:
    status = OrderStatus.INVALID

    # attempt to create a new order
    try:
        user = order_data['user']
        if isinstance(user, int):
            user_id = user
        else:  # assume user is email string
            user_id = UserModel.query.filter_by(email=user).first().id
        order = OrderModel(user=user_id)
        db.session.add(order)
    except (AttributeError, KeyError, sqlalchemy.exc.DBAPIError) as err:
        logger.exception(err)
        db.session.rollback()
        return status

    items = order_data.get('items', [])
    try:
        for item_data in items:
            item = ItemModel.query \
                            .filter_by(id=item_data.get('item_id', None)) \
                            .first()
            if not item:
                item = ItemModel.query \
                                .filter_by(name=item_data['item_name']) \
                                .first()
            quantity = item_data.get('quantity', 1)

            if item.in_stock_quantity - quantity < 0:
                raise StockUnavailableError(f"Only {item.in_stock_quantity} "
                                            f"{item.name}, but {quantity} have"
                                            " been requested")

            order_item = OrderItemModel(order_id=order.id,
                                        item=item.id,
                                        quantity=quantity)
            db.session.add(order_item)
            item.in_stock_quantity -= quantity
        db.session.commit()
        status = OrderStatus.CREATED
    except (AttributeError, TypeError, KeyError, StockUnavailableError) as err:
        logger.exception(err)
        db.session.rollback()
    return status


@store_router.route('/order', methods=['POST'], strict_slashes=False)
def new_order():
    """
    Order creation method.
    ---
    description: Create a new order.
    responses:
      200:
        description: Order successfully created.
      400:
        description: Unable to handle request.
    tags:
        - store
    """
    code = HTTPStatus.OK
    response = {}
    try:
        response = {'status': _create_order(request.json or {})}
    except (AttributeError, TypeError, KeyError, ) as err:
        logger.exception(err)
        code = HTTPStatus.BAD_REQUEST
        response.update({'error': str(err)})
    return Response(response, mimetype='application/json',
                    status=code.value)


@store_router.route('/orders', strict_slashes=False)
@safe_query
def orders():
    """
    List orders retrieval method.
    ---
    description: Retrieve list of orders.
    responses:
      200:
        description: List of orders.
      400:
        description: Unable to handle request.
    tags:
        - store
    """
    query = OrderModel.query.filter_by(**request.args)
    return query_to_json_response(query.all())


@store_router.route('/orders/id/<int:order_id>', methods=['GET'])
@safe_query
def get_order(order_id: int):
    """
    Order data retrieval method.
    ---
    description: Retrieve data associated with specified order.
    parameters:
      - in: path
        name: order_id
        type: integer
        required: true
        description: The unique integer ID representing an order item.
    responses:
      200:
        description: Order details.
      400:
        description: Unable to handle request.
    tags:
        - store
    """
    query = OrderItemModel.query.filter_by(order_id=order_id, **request.args)
    return query_to_json_response(query.all())


def refund(obj: Union[OrderModel, OrderItemModel]):
    """Refund an order."""
    raise NotImplementedError("TODO")


@store_router.route('/orders/id/<int:order_id>', methods=['DELETE'])
@safe_query
def delete_order(order_id: int):
    """
    Void order method.
    ---
    description: Mark order as voided.
    parameters:
      - in: path
        name: order_id
        type: integer
        required: true
        description: The unique integer ID representing an order item.
    responses:
        200:
            description: Order successfully voided.
        400:
            description: Unable to handle request.
        500:
            description: Unhandled exception occurred in server backend.
    tags:
        - store
    """
    order = OrderModel.query.filter_by(order_id=order_id).first()
    if order.status == int(OrderStatus.PAYMENT_RECEIVED):
        order_items = OrderItemModel.query.filter_by(order_id=order_id).all()
        for item in order_items:
            refund(item)  # pylint: disable=redefined-outer-name
        refund(order)
    elif order.status == int(OrderStatus.CREATED):
        order.status = int(OrderStatus.VOIDED)
    else:
        raise NotImplementedError("TODO")

    # confirm
    db.session.commit()
    msg = f'Order {order.id} has been successfully {str(order.status).lower()}'

    return {
        "msg": msg,
        "status": "ok",
        "code": HTTPStatus.OK
    }
