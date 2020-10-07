import pytest
import random

from io import StringIO
from contextlib import redirect_stdout
from unittest.mock import Mock

from online_store.backend.gift_list import AbstractGiftList, BasicGiftList


def test_AbstractGiftList__init__raises_TypeError():
    try:
        abc_giftlist = AbstractGiftList('test')
        assert False  # should not reach here
    except TypeError as err:
        assert "Can't instantiate abstract class" in str(err)


abstract_gift_list_methods = [
    '__init__', 'get_user', 'get_list',
    'create_list', 'create_report',
    'add_item', 'remove_item', 'purchase_item'
]
abstract_gift_list_method_kwargs = [
    {'username_or_id': 'test_user'},
    {'username_or_id': 'test_user'},
    None,
    None,
    None,
    {'item': None},
    {'item': None},
    {'item': None}
]


@pytest.mark.parametrize("method,kwargs",
                         zip(abstract_gift_list_methods,
                             abstract_gift_list_method_kwargs))
def test_BasicGiftList_super_method_raises_NotImplementedError(method, kwargs):
    basic_gift_list = BasicGiftList('test_user')
    assert isinstance(basic_gift_list, AbstractGiftList)
    try:
        func = getattr(super(BasicGiftList, basic_gift_list), method)
        if kwargs is None:
            func()  # some methods do not accept kwargs
        else:
            func(**kwargs)
        assert False
    except NotImplementedError:
        pass  # This is the expected behaviour when calling base method


def test_BasicGiftList__init__():
    giftlist = BasicGiftList('test_user')
    assert isinstance(giftlist, BasicGiftList)
    assert giftlist.gift_list == []
    assert giftlist.user is 'test_user'
    assert not giftlist._availability_map
    assert not giftlist._purchase_map
    assert giftlist._purchase_map[random.random()] == 0


@pytest.mark.parametrize('user', ['test_user', None, 1, -1, 0])
def test_BasicGiftList_get_user(user):
    basic_giftlist = BasicGiftList(user)
    assert basic_giftlist.get_user(user) == user  # NOTE: there are no type checks


def test_BasicGiftList_create_list():
    mock_giftlist = Mock()
    assert not isinstance(mock_giftlist.gift_list, list)
    assert isinstance(BasicGiftList.create_list(mock_giftlist), list)
    assert isinstance(mock_giftlist.gift_list, list)
    assert mock_giftlist.gift_list == []

    # test list is reset on second call
    mock_giftlist.gift_list = [1, 2, 3]
    assert mock_giftlist.gift_list != []
    BasicGiftList.create_list(mock_giftlist)
    assert mock_giftlist.gift_list == []


@pytest.mark.parametrize('item,error_cls,modified_list,available_quantity', [
    ({}, None, [{}], 1),
    ([1, 2, 3], AttributeError, [], 1),          # item should be a dict
    ({'id': 1}, None, [{'id': 1}], 1),
    ({'id': 1}, None, [{'id': 1}], 2),
    ({'id': 1}, ValueError, [{'id': 1}], None),  # quantity should be an int
    ({'id': 1}, ValueError, [{'id': 1}], 3.1),   # quantity should be an int
    ({'id': 1}, ValueError, [{'id': 1}], 0),     # quantity should be a +ve int
    ({'id': 1}, ValueError, [{'id': 1}], 1)      # quantity should be a +ve int
])
def test_BasicGiftList_add_item(item, error_cls, modified_list, available_quantity):
    basic_giftlist = BasicGiftList('test_user')
    assert basic_giftlist.gift_list == []
    assert not basic_giftlist._availability_map
    assert not basic_giftlist._purchase_map

    try:
        # test adding item
        basic_giftlist.add_item(item, available_quantity)
        assert basic_giftlist.gift_list == modified_list
        quantity = basic_giftlist._availability_map[frozenset(item.items())]
        assert quantity == available_quantity
        assert not basic_giftlist._purchase_map  # should not be modified

        # attempt to add item twice
        basic_giftlist.add_item(item, available_quantity)
        assert basic_giftlist.gift_list == modified_list
        quantity = basic_giftlist._availability_map[frozenset(item.items())]
        assert quantity == (2 * available_quantity)
    except AssertionError:
        raise
    except Exception as err:
        assert isinstance(err, error_cls)


@pytest.mark.parametrize('gift_list', [None, {}, (1, 2, 3), 1.0])
def test_BasicGiftList_get_list(gift_list):
    mock_giftlist = Mock()
    mock_giftlist.gift_list = gift_list
    # test that the get_list() method simply returns the gift_list attribute
    assert BasicGiftList.get_list(mock_giftlist) == mock_giftlist.gift_list


@pytest.mark.parametrize('gift_list,item,result,exception', [
    ([None, 1], None, [1], None), 
    ([{'id': 1}, {'id': 2}], {'id': 2}, [{'id': 1}], None),
    ([1, 2, 3], 1, [2, 3], None),
    ([1, 2, 3], 4, [2, 3], ValueError),  # item not in list
    ([2, 2, 2], 2, [2, 2], None),
    ((1, 2), 2, (1, 2), AttributeError)  # gift_list is not a list
])
def test_BasicGiftList_remove_item(gift_list, item, result, exception):
    mock_giftlist = Mock()
    mock_giftlist.gift_list = gift_list
    try:
        BasicGiftList.remove_item(mock_giftlist, item)
        assert mock_giftlist.gift_list == result
    except AssertionError:
        raise
    except Exception as err:
        assert isinstance(err, exception)


@pytest.mark.parametrize(
    'gift_list,item,quantity_available,quantity_to_purchase,exception', [
    ([{'id': 1}], {'id': 1}, 1, 1, None),
    ([{'id': 1}], {'id': 1}, 0, 1, ValueError),  # not enough availability
])
def test_BasicGiftList_purchase_item(
    gift_list, item, quantity_available, quantity_to_purchase, exception):
    basic_giftlist = BasicGiftList('test_user')
    try:
        key = frozenset(item.items())
        assert not basic_giftlist.gift_list
        basic_giftlist.gift_list = gift_list
        assert basic_giftlist.gift_list == gift_list
        assert not basic_giftlist._availability_map
        basic_giftlist._availability_map[key] = quantity_available
        assert basic_giftlist._availability_map[key] == quantity_available
        assert basic_giftlist._purchase_map[key] == 0
        basic_giftlist.purchase_item(item, quantity_to_purchase)
        assert basic_giftlist._availability_map[key] == \
            quantity_available - quantity_to_purchase
        assert basic_giftlist._purchase_map[key] == quantity_to_purchase
    except AssertionError:
        raise
    except Exception as err:
        if not isinstance(err, exception):
            raise  # recover traceback for debugging


@pytest.mark.parametrize(
    'user,gift_list,purchased_items,available_items', [
    ('test_user', [], [], []),
    ('test_user', [{'id': 1}], [({'id': 1}, 2)], [({'id': 1}, 1)]),
    ('test_user', [{'id': 1}, {'id': 2}], 
     [({'id': 1}, 2), ({'id': 2}, 1)], [({'id': 1}, 1), ({'id': 2}, 0)])
])
def test_BasicGiftList_create_report(
    user, gift_list, purchased_items, available_items
):
    basic_giftlist = BasicGiftList(user)

    basic_giftlist.gift_list = gift_list
    assert basic_giftlist.gift_list == gift_list

    # set availability and purchase amounts
    for item, quantity in purchased_items:
        basic_giftlist._purchase_map[frozenset(item.items())] = quantity
    for item, quantity in available_items:
        basic_giftlist._availability_map[frozenset(item.items())] = quantity

    with StringIO() as buf, redirect_stdout(buf):
        basic_giftlist.create_report()
        report = buf.getvalue()
    
    for section, items in [('Purchased items:', purchased_items),
                           ('Available items:', available_items)]:
        assert section in report
        section_index = report.index(section)
        for item, quantity in items:
            item_line = f'{item} (quantity: {quantity})'
            if quantity:
                assert item_line in report
                assert report.index(item_line) > section_index
            else:
                assert item_line not in report
   
    assert user in report
