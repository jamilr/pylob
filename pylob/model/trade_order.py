from dataclasses import dataclass
from decimal import Decimal
from enum import Enum

from pylob.model import Side


class OrderType(Enum):
    MARKET = 1
    LIMIT = 2


@dataclass
class TradeOrder:
    order_type: OrderType
    side: Side
    quantity: int


@dataclass
class MarketOrder(TradeOrder):

    @staticmethod
    def create(order: TradeOrder) -> 'MarketOrder':
        return MarketOrder(order.order_type, order.side, order.quantity)

    def __str__(self):
        return f'MarketOrder(type={self.order_type.name}, side={self.side.name}, quantity={self.quantity})'


@dataclass
class LimitOrder(TradeOrder):
    price: Decimal
