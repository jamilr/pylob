from enum import IntEnum
from decimal import Decimal
from dataclasses import dataclass
from typing import Optional

class Side(IntEnum):
    BUY = 1
    SELL = 2

@dataclass
class Order:
    """
    Order - a market order data model. id is Optional since it is updated by the OrderBook.
    It is a doubly-linked node supporting a lookup for a previous or a next order.
    """

    side: Side
    price: Decimal
    quantity: int = 0
    id: Optional[int] = None
    prev_order: Optional['Order'] = None
    next_order: Optional['Order'] = None

    def update(self, new_qty: int):
        self.quantity = new_qty

    def __str__(self):
        return f"Order({self.side.name}, {self.price}, {self.quantity}, {self.id})"

