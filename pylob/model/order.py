from enum import IntEnum
from decimal import Decimal
from dataclasses import dataclass
from typing import Optional

class Side(IntEnum):
    BUY = 1
    SELL = 2

@dataclass
class Order:
    id: int
    side: Side
    price: Optional[Decimal] = None
    quantity: int = 0
    prev_order: Optional['Order'] = None
    next_order: Optional['Order'] = None

    def update(self, new_qty: int):
        self.quantity = new_qty

    def __str__(self):
        return f"Order({self.id}, {self.side.name}, {self.price}, {self.quantity})"

