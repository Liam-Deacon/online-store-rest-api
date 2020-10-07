import pytest
from unittest.mock import Mock

import online_store.backend.gift_list as gift_list
from online_store.backend.gift_list import AbstractGiftList, BasicGiftList


def test_AbstractGiftList__init__raises_TypeError():
    try:
        abc_giftlist = gift_list.AbstractGiftList('test')
        assert False  # should not reach here
    except TypeError as err:
        assert "Can't instantiate abstract class" in str(err)


abstract_gift_list_methods = [
    '__init__', 'get_user', 'create_list', 'create_report',
    'add_item', 'remove_item', 'purchase_item'
]
abstract_gift_list_method_kwargs = [
    {'username_or_id': 'test_user'},
    {'username_or_id': 'test_user'},
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
    basic_gift_list = gift_list.BasicGiftList('test_user')
    assert isinstance(basic_gift_list, AbstractGiftList)
    try:
        func = getattr(super(gift_list.BasicGiftList, basic_gift_list), method)
        if kwargs is None:
            func()  # some methods do not accept kwargs
        else:
            func(**kwargs)
        assert False
    except NotImplementedError:
        pass  # This is the expected behaviour when calling base method


def test_BasicGiftList__init__():
    giftlist = gift_list.BasicGiftList('test_user')
    assert isinstance(giftlist, BasicGiftList)
    assert giftlist.gift_list == []
    assert giftlist.user is 'test_user'
    assert not giftlist._availability_map
    assert not giftlist._purchase_map


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
        basic_giftlist.add_item(item, available_quantity)
        assert basic_giftlist.gift_list == modified_list
        quantity = basic_giftlist._availability_map[frozenset(item.items())]
        assert quantity == available_quantity
        assert not basic_giftlist._purchase_map  # should not be modified
    except AssertionError:
        raise
    except Exception as err:
        assert isinstance(err, error_cls)

