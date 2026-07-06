import pytest

from pylob.model import Order, Side
from decimal import Decimal


class TestOrder:

    @pytest.fixture
    def simple_order(self) -> Order:
        return Order(id=1, price=Decimal(50.0), side = Side.BUY, quantity=100)

    def test_update(self, simple_order):
        assert simple_order.id == 1
        assert simple_order.price == 50.0
        assert simple_order.side == Side.BUY
        assert simple_order.quantity == 100

        simple_order.update(300)
        assert simple_order.quantity == 300

