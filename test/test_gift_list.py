import pytest

import online_store.backend.gift_list as gift_list
from online_store.backend.gift_list import AbstractGiftList


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
    giftlist = gift_list.AbstractGiftList
