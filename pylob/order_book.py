from dataclasses import dataclass
from decimal import Decimal, getcontext
from typing import List, Tuple

from pylob.model import Order, Side, OrderList
from pylob.model.order_tree import OrderTree
from pylob.model.trade import Trade
from pylob.model import MarketOrder, LimitOrder, OrderType
from pylob.order_book_helper import OrderBookHelper

getcontext().prec = 6


@dataclass
class OrderExecutionResult:
    trades: List[Trade]
    quantity: int = 0

    def __post_init__(self):
        self.quantity = sum(trade.quantity for trade in self.trades)

    @property
    def vwap(self) -> Decimal:
        return OrderBookHelper.vwap(self.trades)


class OrderBook:
    __USE_BUILTIN_ORDER_ID__ = True

    def __init__(self):
        self.bids = OrderTree()
        self.asks = OrderTree()
        self._last_order_id = 0
        self.vwap = OrderBookHelper.vwap

    def best_bid_price(self):
        return self.bids.max_price()

    def best_ask_price(self):
        return self.asks.min_price()

    def bids_depth(self) -> int:
        return self.bids.depth()

    def asks_depth(self) -> int:
        return self.asks.depth()

    def best_ask_price_list(self) -> OrderList:
        best_ask_price = self.best_ask_price()
        return self.asks.price_map[best_ask_price]

    def best_bid_price_list(self) -> OrderList:
        best_bid_price = self.best_bid_price()
        return self.bids.price_map[best_bid_price]

    def add(self, order: Order):
        if self.__USE_BUILTIN_ORDER_ID__ and order.id is None:
            order.id = self._next_order_id()
        if order.side == Side.BUY:
            self.bids.add_order(order)
        else:
            self.asks.add_order(order)

    def remove(self, order: Order):
        if order.side == Side.SELL:
            self.asks.remove_order(order)
        else:
            self.bids.remove_order(order)

    def execute(self, order_to_trade: MarketOrder | LimitOrder) -> OrderExecutionResult:
        exec_mkt_order = self._execute_market_order
        exec_lmt_order = self._execute_limit_order
        executed_trades = exec_mkt_order(order_to_trade) if isinstance(order_to_trade, MarketOrder) else exec_lmt_order(
            order_to_trade)
        return OrderExecutionResult(trades=executed_trades)

    def _execute_market_order(self, order: MarketOrder):
        executed_trades: List[Trade] = []
        quantity_to_trade, side = order.quantity, order.side
        if side == Side.BUY:
            while self.asks and quantity_to_trade > 0:
                best_ask_price_order_list = self.best_ask_price_list()
                quantity_to_trade, trades = self._match(quantity_to_trade, best_ask_price_order_list)
                executed_trades.extend(trades)
        else:
            while self.bids and quantity_to_trade > 0:
                best_bid_price_order_list = self.best_bid_price_list()
                quantity_to_trade, trades = self._match(quantity_to_trade, best_bid_price_order_list)
                executed_trades.extend(trades)
        return executed_trades

    def _match(self, quantity_to_trade: int, order_list: OrderList) -> Tuple[int, List[Trade]]:
        trades: List[Trade] = []
        while quantity_to_trade > 0 and order_list:
            to_remove = False
            order: Order = order_list.head_order
            if quantity_to_trade < order.quantity:
                residual = order.quantity - quantity_to_trade
                order.update(residual)
                order_list.move_to_tail(order)
                traded_quantity = quantity_to_trade
                quantity_to_trade = 0
            elif quantity_to_trade == order.quantity:
                traded_quantity = quantity_to_trade
                quantity_to_trade = 0
                to_remove = True
            else:
                quantity_to_trade = quantity_to_trade - order.quantity
                traded_quantity = order.quantity
                to_remove = True
            trades.append(Trade(price=order.price, quantity=traded_quantity))
            if to_remove:
                self.remove(order)
        return quantity_to_trade, trades

    def _execute_limit_order(self, order: LimitOrder) -> List[Trade]:
        executed_trades, qty_to_trade = [], order.quantity
        if order.side == Side.SELL:
            while self.bids and self.best_bid_price() > order.price and qty_to_trade > 0:
                best_bid_price_order_list = self.best_bid_price_list()
                qty_to_trade, trades = self._match(qty_to_trade, best_bid_price_order_list)
                executed_trades.extend(trades)
            if qty_to_trade > 0:
                self.add(Order(side=Side.SELL, price=order.price, quantity=qty_to_trade))
        else:
            while self.asks and order.price > self.best_ask_price() and qty_to_trade > 0:
                best_ask_price_order_list = self.best_ask_price_list()
                qty_to_trade, trades = self._match(order.quantity, best_ask_price_order_list)
                executed_trades.extend(trades)
            if qty_to_trade > 0:
                self.add(Order(side=Side.BUY, price=order.price, quantity=qty_to_trade))
        return executed_trades

    def _next_order_id(self) -> int:
        id_to_return = self._last_order_id
        self._last_order_id += 1
        return id_to_return

    def __str__(self):
        return f'OrderBook(bids={self.bids}, asks={self.asks})'


if __name__ == '__main__':
    obook = OrderBook()
    orders = [Order(Side.BUY, Decimal(122), 100),
              Order(Side.BUY, Decimal(122), 100),
              Order(Side.BUY, Decimal(124), 100),
              Order(Side.BUY, Decimal(124), 200),
              Order(Side.BUY, Decimal(125), 100),
              Order(Side.BUY, Decimal(125), 200),
              Order(Side.SELL, Decimal(130), 200),
              Order(Side.SELL, Decimal(134), 100)]
    for o in orders:
        obook.add(o)

    print(obook)
    print(f'{obook.best_bid_price()} {obook.best_ask_price()}')
    mkt_order = MarketOrder(OrderType.MARKET, Side.BUY, 250)

    print(f'{mkt_order}')
    qty, price = obook.execute(mkt_order)
    print(f'price={price}, qty={qty}')
    print(f'B={obook.best_bid_price()} A={obook.best_ask_price()}')
