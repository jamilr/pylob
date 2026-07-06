from decimal import Decimal
from typing import List

import pytest

from pylob.model import Order, Side
from pylob.order_book import OrderBook, MarketOrder, OrderType, LimitOrder
from pylob.order_book_helper import OrderBookHelper
from tests.base_test import BaseTestOrderBook


class TestOrderBook:

    @pytest.fixture
    def order_book(self) -> OrderBook:
        return OrderBook()

    @pytest.fixture
    def random_buy_orders(self) -> List[Order]:
        return [
            Order(Side.BUY, Decimal(100.0), 50),
            Order(Side.BUY, Decimal(100.0), 30),
            Order(Side.BUY, Decimal(120.0), 35),
            Order(Side.BUY, Decimal(125.0), 40),
        ]

    @pytest.fixture
    def random_sell_orders(self) -> List[Order]:
        return [
            Order(Side.SELL, Decimal(126.0), 50),
            Order(Side.SELL, Decimal(127.0), 30),
            Order(Side.SELL, Decimal(129.0), 35),
            Order(Side.SELL, Decimal(130.0), 40),
        ]

    @pytest.fixture
    def market_order(self) -> MarketOrder:
        return MarketOrder(OrderType.MARKET, Side.BUY, 100)

    @pytest.fixture
    def limit_order(self) -> LimitOrder:
        return LimitOrder(OrderType.LIMIT, Side.SELL, 100, Decimal(99.0))

    @pytest.fixture
    def orders_from_csv(self) -> List[Order]:
        return OrderBookHelper.to_orders(BaseTestOrderBook().base_test_raw_order_values())

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

    def test_execute_limit_order_full_fill(self, order_book, orders_from_csv, limit_order):
        for order in orders_from_csv:
            order_book.add(order)
        qty, vwap = order_book.execute(limit_order)
        assert qty == 100
        assert vwap == Decimal(100.0)

    def test_execute_sell_limit_order_partial_fill(self, order_book, orders_from_csv):
        for order in orders_from_csv:
            order_book.add(order)
        assert order_book.best_bid_price() == Decimal(100.0)
        assert order_book.best_ask_price() == Decimal(105.0)
        limit_order = LimitOrder(OrderType.LIMIT, Side.SELL, 200, Decimal(99.0))
        qty, vwap = order_book.execute(limit_order)
        assert qty == 100
        assert vwap == Decimal(100.0)
        assert order_book.best_bid_price() == Decimal(90.0)
        assert order_book.best_ask_price() == Decimal(99.0)

    def test_execute_buy_limit_order_partial_fill(self, order_book, orders_from_csv):
        for order in orders_from_csv:
            order_book.add(order)
        assert order_book.best_bid_price() == Decimal(100.0)
        assert order_book.best_ask_price() == Decimal(105.0)
        limit_order = LimitOrder(OrderType.LIMIT, Side.BUY, 200, Decimal(106.0))
        qty, vwap = order_book.execute(limit_order)
        assert qty == 100
        assert vwap == Decimal(105.0)
        assert order_book.best_bid_price() == Decimal(106.0)
        assert order_book.best_ask_price() == Decimal(110.0)