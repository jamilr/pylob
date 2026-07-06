from decimal import Decimal

import pytest

from pylob.model import Side, Order, OrderTree


class TestOrderTree:

    @pytest.fixture
    def random_buy_orders(self):
        return [
            Order(Side.BUY, Decimal(100.0), 50),
            Order(Side.BUY, Decimal(100.0), 30),
            Order(Side.BUY, Decimal(120.0), 35),
            Order(Side.BUY, Decimal(125.0), 40),
        ]

    def test_order_depth(self, random_buy_orders):
        order_tree = OrderTree()
        for order in random_buy_orders:
            order_tree.add_order(order)
        assert order_tree.depth() == 3
        assert order_tree.min_price() == Decimal(100.0)
        assert order_tree.max_price() == Decimal(125.0)
