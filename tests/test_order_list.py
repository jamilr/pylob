import pytest
from typing import List
from pylob.model import Order, Side, OrderList
from decimal import Decimal


class TestOrderList:

    @pytest.fixture
    def order_list(self) -> OrderList:
        return OrderList()

    @pytest.fixture
    def single_order(self) -> Order:
        return Order(1, Side.BUY, Decimal(100.0), 100)

    @pytest.fixture
    def same_price_buy_orders(self) -> List[Order]:
        return [
            Order(1, Side.BUY, Decimal(100.0), 50),
            Order(2, Side.BUY, Decimal(100.0), 30),
            Order(3, Side.BUY, Decimal(100.0), 35),
            Order(4, Side.BUY, Decimal(100.0), 40),
        ]

    @pytest.fixture
    def same_price_sell_orders(self) -> List[Order]:
        return [
            Order(1, Side.SELL, Decimal(100.0), 50),
            Order(2, Side.SELL, Decimal(100.0), 30),
            Order(3, Side.SELL, Decimal(100.0), 35),
            Order(4, Side.SELL, Decimal(100.0), 45),
        ]

    @pytest.fixture
    def order_list_with_single_order(self, order_list: OrderList, single_order) -> OrderList:
        order_list.append(single_order)
        return order_list

    @pytest.fixture
    def order_list_with_buy_orders(self, order_list, same_price_buy_orders):
        for order in same_price_buy_orders:
            order_list.append(order)
        return order_list

    @pytest.fixture
    def order_list_with_sell_orders(self, order_list, same_price_sell_orders):
        for order in same_price_sell_orders:
            order_list.append(order)
        return order_list

    def test_order_list_with_a_single_order(self, order_list_with_single_order):
        order_list = order_list_with_single_order
        assert len(order_list) == 1
        assert order_list.volume == 100

    def test_order_list_with_buy_orders(self, order_list_with_buy_orders):
        order_list = order_list_with_buy_orders
        assert len(order_list) == 4
        assert order_list.volume == 155

    def test_order_list_with_sell_orders(self, order_list_with_sell_orders):
        order_list = order_list_with_sell_orders
        assert len(order_list) == 4
        assert order_list.volume == 160

    def test_remove_order(self, order_list_with_buy_orders, same_price_buy_orders):
        order_list = order_list_with_buy_orders
        orders = same_price_buy_orders
        assert len(order_list) == 4
        order_list.remove(orders[2])
        assert len(order_list) == 3


