from decimal import Decimal

from pylob.model.order import Order, Side


class OrderList:
    """ OrderList - a double-linked list of orders """

    def __init__(self):
        self.head_order = None
        self.tail_order = None
        self.volume = 0
        self.length = 0
        self.last = None

    def __len__(self):
        return self.length

    def __iter__(self):
        self.last = self.head_order
        return self

    def next(self):
        if self.last is None:
            raise StopIteration
        cur_order = self.last
        self.last = self.last.next_order
        return cur_order

    __next__ = next

    def append(self, order: Order) -> Order:
        if len(self) == 0:
            self.head_order = order
            self.tail_order = order
        else:
            order.prev_order = self.tail_order
            order.next_order = None
            self.tail_order.next_order = order
            self.tail_order = order
        self.volume += order.quantity
        self.length += 1
        return order

    def remove(self, order: Order):
        prev_order = order.prev_order
        next_order = order.next_order
        if prev_order is not None and next_order is not None:
            prev_order.next_order = next_order
            next_order.prev_order = prev_order
        elif prev_order is not None:
            prev_order.next_order = None
            self.tail_order = prev_order
        elif next_order is not None:
            next_order.prev_order = None
            self.head_order = next_order
        self.volume -= order.quantity
        self.length -= 1

    def move_to_tail(self, order: Order):
        if len(self) != 0:
            self.remove(order)
        self.append(order)

    def __str__(self):
        return f'{self.volume}'

    @staticmethod
    def print(order_list):
        for order in order_list:
            print(order)


if __name__ == '__main__':
    order_list = OrderList()
    orders = [Order(1, Side.BUY, Decimal(124), 100),
              Order(2, Side.SELL, Decimal(125), 100),
              Order(3, Side.BUY, Decimal(130), 200)]
    for o in orders:
        order_list.append(o)
    OrderList.print(order_list)
    order_list.move_to_tail(orders[1])
    OrderList.print(order_list)
