from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Trade:
    quantity: int
    price: Decimal | None = None
