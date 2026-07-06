from decimal import Decimal
from typing import List

import pytest

from pylob.model import Trade, Side, Order
from pylob.order_book_helper import OrderBookHelper
from tests.base_test import BaseTestOrderBook


class TestOrderBookHelper:
    """ Test cases class for OrderBookHelper """

    @pytest.fixture
    def executed_trades(self) -> List[Trade]:
        return [
            Trade(500, Decimal(120.0)),
            Trade(500, Decimal(100.0)),
            Trade(500, Decimal(80.0)),
        ]

    @pytest.fixture
    def test_orders_list(self) -> List[Order]:
        return OrderBookHelper.to_orders(BaseTestOrderBook().base_test_raw_order_values())

    def test_vwap(self, executed_trades):
        vwap_price = OrderBookHelper.vwap(executed_trades)
        assert vwap_price == Decimal("100.0")

    def test_to_order(self, test_orders_list):
        orders = test_orders_list
        assert len(list(filter(lambda x: x.side == Side.BUY, orders))) == 6
        assert len(list(filter(lambda x: x.side == Side.SELL, orders))) == 6
