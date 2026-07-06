from collections import defaultdict

from sortedcontainers import SortedDict

from pylob.model import Order, OrderList


class OrderTree:

    def __init__(self):
        self.price_map = SortedDict()
        self.order_map = defaultdict(Order)

    def depth(self):
        return len(self.price_map)

    def min_price(self):
        if self.price_map:
            return self.price_map.keys()[0]
        return None

    def max_price(self):
        if self.price_map:
            return self.price_map.keys()[-1]
        return None

    def add_order(self, order: Order):
        if order.price not in self.price_map:
            self.price_map[order.price] = OrderList()
        updated_order = self.price_map[order.price].append(order)
        self.order_map[updated_order.id] = order

    def remove_order(self, order: Order):
        self.price_map[order.price].remove(order)
        if len(self.price_map[order.price]) == 0:
            del self.price_map[order.price]
        self.order_map.pop(order.id)

    def cancel_order(self, order_id: int):
        if order_id not in self.order_map:
            raise ValueError(f'Order with id={order_id} not found.')
        order_to_remove = self.order_map.pop(order_id)
        self.price_map[order_to_remove.price].remove(order_to_remove)
        if len(self.price_map[order_to_remove.price]) == 0:
            del self.price_map[order_to_remove.price]

    def __str__(self):
        return f'OrderTree(' + ','.join([f'{key}:{val}' for key, val in self.price_map.items()]) + ')'