import context
import unittest
import decimal
from sheets import *

class TestMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.wb = Workbook()
        _, self.s1 = self.wb.new_sheet()
        _, self.s2 = self.wb.new_sheet()

    def test_loop_0(self):
        self.wb.set_cell_contents(self.s1, 'a1', '=a1')
        a1_v = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_v, CellError)
        self.assertEqual(a1_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)

    def test_loop_1(self):
        self.wb.set_cell_contents(self.s1, 'a1', '=a2')
        self.wb.set_cell_contents(self.s1, 'a2', '=a1')
        a1_v = self.wb.get_cell_value(self.s1, 'a1')
        a2_v = self.wb.get_cell_value(self.s1, 'a2')
        self.assertIsInstance(a1_v, CellError)
        self.assertEqual(a1_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertIsInstance(a2_v, CellError)
        self.assertEqual(a2_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
    
    def test_loop_remove(self):
        self.wb.set_cell_contents(self.s1, 'a1', '=a2')
        self.wb.set_cell_contents(self.s1, 'a2', '=a1')
        a1_v = self.wb.get_cell_value(self.s1, 'a1')
        a2_v = self.wb.get_cell_value(self.s1, 'a2')
        self.assertIsInstance(a1_v, CellError)
        self.assertEqual(a1_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertIsInstance(a2_v, CellError)
        self.assertEqual(a2_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.wb.set_cell_contents(self.s1, 'a2', '=1')
        a1_v = self.wb.get_cell_value(self.s1, 'a1')
        a2_v = self.wb.get_cell_value(self.s1, 'a2')
        self.assertEqual(a1_v, decimal.Decimal(1))
        self.assertEqual(a1_v, decimal.Decimal(1))

if __name__ == '__main__':
    unittest.main()
