from decimal import Decimal
from typing import List, Optional

from pylob.model import Order, Side
from pylob.model.trade import Trade


class OrderBookHelper:

    @staticmethod
    def vwap(trades: List[Trade]) -> Decimal:
        """ Returns the VWAP price for the list of trades """
        num, total_qty = 0, 0
        for trade in trades:
            num += trade.quantity * trade.price
            total_qty += trade.quantity
        return Decimal(num / total_qty)

    @staticmethod
    def to_order(raw_values: list[str]) -> Optional[Order]:
        if len(raw_values) < 3:
            return None
        validate_input = all([isinstance(val, str) for val in raw_values])
        if not validate_input:
            raise ValueError(f'Some or all input values are invalid. {raw_values}')
        side_int = int(raw_values[0])
        if side_int not in Side:
            return None
        side = Side(side_int)
        price = Decimal(raw_values[1])
        if price < 0.0:
            return None
        qty = int(raw_values[2])
        if qty <= 0:
            return None
        return Order(side, price, qty)

    @staticmethod
    def to_orders(raw_values: list[list[str]]) -> List[Order]:
        orders: List[Order] = []
        for record in raw_values:
            order = OrderBookHelper.to_order(record)
            if order:
                orders.append(order)
        return orders
