from online_store.backend.models.order import OrderStatus


def test_OrderStatus_str():
    assert OrderStatus.CREATED.name == str(OrderStatus(OrderStatus.CREATED))
    assert OrderStatus.CREATED.name != str(OrderStatus(OrderStatus.INVALID))


def test_OrderStatus_int():
    assert OrderStatus.CREATED.value == int(OrderStatus(OrderStatus.CREATED))
    assert OrderStatus.CREATED.value != int(OrderStatus(OrderStatus.INVALID))
