"""Defines the API routes for user gift lists."""
from http import HTTPStatus
from flask import Blueprint, jsonify, request, Response
from flask_jwt_extended import get_jwt_identity, jwt_required

from ..utils.query import query_to_json_response, safe_query
from ..models.user import UserModel

from ..gift_list import AbstractGiftList, GiftListFactory

gifts_router = Blueprint('gifts', __name__, url_prefix='/gifts')  # pylint: disable=invalid-name


def get_user() -> UserModel:
    """Get the UserModel given by current scoped JWT identity."""
    return UserModel.query.filter_by(username=get_jwt_identity()).first()


def get_giftlist() -> AbstractGiftList:
    """Simple convenience function for getting GiftList for current user."""
    return GiftListFactory(get_user(), gift_list_cls='sql')


@gifts_router.route('/list/report')
@jwt_required
def gift_report() -> Response:
    """
    Produce report of purchased and non-purchased gifts within user list.
    ---
    description: Produce report of user's gift list.
    responses:
      200:
        description: JSON report successfully generated.
      204:
        description: No gifts in user's list.
    tags:
      - gifts
    """
    gift_list: AbstractGiftList = get_giftlist()
    return jsonify(gift_list.create_report()), HTTPStatus.OK


@gifts_router.route('/list/add', methods=['POST'])
@jwt_required
def add_gift() -> Response:
    """
    Add a gift to the user's gift list.
    ---
    description: Add gift to user list.
    security:
      - bearerAuth: []
    parameters:
      - name: item_id
        in: query
        type: integer
        required: true
        description: The unique integer ID representing a store item.
      - name: quantity
        in: query
        type: integer
        required: false
        description: Number of desired (available) gifts of this item.
    responses:
      200:
        description: Item successfully added.
      400:
        description: Unable to add item to list.
    tags:
      - gifts
    """
    msg, status, code = "Item added", "ok", HTTPStatus.OK
    data = request.args
    gift_list = get_giftlist()
    if not gift_list.add_item(data):
        msg, status, code = \
            "Unable to add item", "error", HTTPStatus.BAD_REQUEST
    return jsonify({'msg': msg, "status": status, "code": code}), code


@gifts_router.route('/list/<gift_id>', methods=['GET'])
@jwt_required
@safe_query
def get_gift(gift_id: int) -> Response:
    """
    Retrieve gift information.
    ---
    description: Retrieve information on gift.
    security:
      - bearerAuth: []
    parameters:
      - name: gift_id
        in: path
        type: integer
        required: true
        description: The unique integer ID representing a gift item.
    responses:
      200:
        description: Successfuly returned gift item data.
        content:
          application/json:
            type: object
            properties:
              id:
                type: integer
                description: The gift item ID.
              item_id:
                type: string
                description: The item store ID.
              list_id:
                type: integer
                description: The gift list ID.
              available:
                type: integer
                description: Desired number of gift item yet to purchase.
              purchased:
                type: integer
                description: Amount of gift item purchased.
    tags:
      - gifts
    """
    gift = get_giftlist().get_list().filter_by(id=gift_id).first()
    return query_to_json_response(gift)


@gifts_router.route('/list/<gift_id>', methods=['DELETE'])
@jwt_required
@safe_query
def remove_gift(gift_id: int) -> Response:
    """
    Remove gift from user's gift list.
    ---
    parameters:
      - name: gift_id
        in: path
        type: integer
        required: true
    security:
      - bearerAuth: []
    tags:
      - gifts
    """
    gift = get_giftlist().remove_item(gift_id)  # pylint: disable=unused-variable; noqa
    # TODO: check that gift belongs to user, stop if not
    return jsonify({"msg": "Gift removed from list",
                    "status": "ok", "code": HTTPStatus.OK}), HTTPStatus.OK


@gifts_router.route('/list/<gift_id>/purchase', methods=['POST'])
@safe_query
@jwt_required
def purchase_gift(gift_id: int) -> Response:
    """
    Purchase gift from list.
    ---
    description: Purchase the gift
    parameters:
      - name: gift_id
        in: path
        type: integer
        required: true
        description: The unique gift item ID.
      - name: quantity
        in: query
        type: integer
        required: false
        description: The quantity of the gift to purchase (default is 1).
    security:
      - bearerAuth: []
    tags:
      - gifts
    """
    gift = get_giftlist().get_list().filter_by(id=gift_id).first()
    quantity = request.args.get('quantity', type=int, default=1)
    get_giftlist().purchase_item(gift, quantity)
    return jsonify(msg="gift purchased",
                   status='ok',
                   code=HTTPStatus.OK), HTTPStatus.OK


@gifts_router.route('/list')
@jwt_required
def list_gifts() -> Response:
    """
    List all gifts added to user's gift list.
    ---
    security:
      - bearerAuth: []
    description: Return the user's gift list data.
    tags:
      - gifts
    """
    gift_list = get_giftlist()
    items = [gift_list.item_as_json(item) for item in gift_list.get_list()]
    return jsonify(items), HTTPStatus.OK if items else HTTPStatus.NO_CONTENT
