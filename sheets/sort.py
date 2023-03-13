'''
The sort module handles sorting rows for sheets by creating an adapter for
a row in a sheet to be used in python's standard sort function.
'''
import decimal
from .cellerror import CellError

_TYPE_VALUE = {
    bool: 2,
    str: 1,
    decimal.Decimal: 0,
    None: -1
}

def order(col):
    '''
    Function to assign whether a column is in ascending or descending order
    '''
    if col < 0:
        return lambda x : not x
    return lambda x : x

class Row():
    '''
    A representation for a row within a sheet to be used in sort.
    '''
    def __init__(self, row_loc) -> None:
        self.row_loc = row_loc
        self.orders = []
        self.values = []

    def add_column_order(self, col: int):
        '''
        Add the order (ascending/descending) for the column
        '''
        self.orders.append(order(col))

    def add_column_value(self, val):
        '''
        Add a column value for comparison
        '''
        self.values.append(val)

    def _is_valid_operand(self, other) -> bool:
        if not hasattr(other, "values"):
            return False
        return len(other.values) == len(self.values)

    def __eq__(self, other: object) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        return self.values == other.values

    def __lt__(self, other: object) -> bool:
        if not self._is_valid_operand(other):
            return NotImplemented
        for i, self_val in enumerate(self.values):
            col_order = self.orders[i]
            other_val = other.values[i]
            if type(self_val) is type(other_val):
                if self_val is None:
                    return False
                if isinstance(self_val, CellError):
                    self_val = self_val.get_type().value
                    other_val = other_val.get_type().value
                if isinstance(self_val, str):
                    self_val = self_val.lower()
                    other_val = other_val.lower()
                if self_val == other_val:
                    continue
                return col_order(self_val < other_val)
            type_val1 = _TYPE_VALUE[type(self_val)]
            type_val2 = _TYPE_VALUE[type(other_val)]
            if type_val1 == type_val2:
                continue
            return col_order(type_val1 < type_val2)
        return False
