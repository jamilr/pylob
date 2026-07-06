import csv
from typing import List


class BaseTestOrderBook:
    __test_orders_file__ = 'test_orders.csv'

    def base_test_raw_order_values(self) -> List[List[str]]:
        raw_order_values: List[List[str]] = []
        with open(f'./tests/{self.__test_orders_file__}', 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                raw_order_values.append(row)
        return raw_order_values
