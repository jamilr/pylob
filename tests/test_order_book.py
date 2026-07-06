from decimal import Decimal
from typing import List

import pytest

from pylob.model import Order, Side
from pylob.order_book import OrderBook, MarketOrder, OrderType


class TestOrderBook:

    @pytest.fixture
    def order_book(self) -> OrderBook:
        return OrderBook()

    @pytest.fixture
    def random_buy_orders(self) -> List[Order]:
        return [
            Order(1, Side.BUY, Decimal(100.0), 50),
            Order(2, Side.BUY, Decimal(100.0), 30),
            Order(3, Side.BUY, Decimal(120.0), 35),
            Order(4, Side.BUY, Decimal(125.0), 40),
        ]

    @pytest.fixture
    def random_sell_orders(self) -> List[Order]:
        return [
            Order(1, Side.SELL, Decimal(126.0), 50),
            Order(2, Side.SELL, Decimal(127.0), 30),
            Order(3, Side.SELL, Decimal(129.0), 35),
            Order(4, Side.SELL, Decimal(130.0), 40),
        ]

    @pytest.fixture
    def market_order(self) -> MarketOrder:
        return MarketOrder(OrderType.MARKET, Side.BUY, 100)

    def test_best_bid_best_ask(self, order_book, random_buy_orders, random_sell_orders):
        for order in random_buy_orders + random_sell_orders:
            order_book.add(order)

        assert order_book.best_bid_price() == Decimal(125.0)
        assert order_book.best_ask_price() == Decimal(126.0)

    def test_execute_market_order(self, order_book, market_order, random_buy_orders, random_sell_orders):
        for order in random_buy_orders + random_sell_orders:
            order_book.add(order)

        assert order_book.bids_depth() == 3
        assert order_book.asks_depth() == 4
        qty_traded, vwap_price = order_book.execute(market_order)
        assert qty_traded == 100
        assert vwap_price > Decimal(126.0)
        assert order_book.best_bid_price() == Decimal(125.0)
        assert order_book.best_ask_price() == Decimal(129.0)
        assert order_book.bids_depth() == 3
        assert order_book.asks_depth() == 2

