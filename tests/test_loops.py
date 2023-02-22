# pylint: skip-file
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

    def test_loop_2(self):
        self.wb.set_cell_contents(self.s1, 'a1', '=a2')
        self.wb.set_cell_contents(self.s1, 'a2', '=a3')
        self.wb.set_cell_contents(self.s1, 'a3', '=a4')
        self.wb.set_cell_contents(self.s1, 'a4', '=a1')
        a1_v = self.wb.get_cell_value(self.s1, 'a1')
        a2_v = self.wb.get_cell_value(self.s1, 'a2')
        a3_v = self.wb.get_cell_value(self.s1, 'a3')
        a4_v = self.wb.get_cell_value(self.s1, 'a4')
        self.assertIsInstance(a1_v, CellError)
        self.assertEqual(a1_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertIsInstance(a2_v, CellError)
        self.assertEqual(a2_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertIsInstance(a3_v, CellError)
        self.assertEqual(a3_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertIsInstance(a4_v, CellError)
        self.assertEqual(a4_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)

    def test_loop_3(self):
        self.wb.set_cell_contents(self.s1, 'a1', '=a2')
        self.wb.set_cell_contents(self.s1, 'a2', '=a3')
        self.wb.set_cell_contents(self.s1, 'a3', '=a4')
        self.wb.set_cell_contents(self.s1, 'a4', '=a1')
        self.wb.set_cell_contents(self.s1, 'b1', '=b2')
        self.wb.set_cell_contents(self.s1, 'b2', '=b3')
        self.wb.set_cell_contents(self.s1, 'b3', '=b4')
        self.wb.set_cell_contents(self.s1, 'b4', '=b1')
        a1_v = self.wb.get_cell_value(self.s1, 'a1')
        a2_v = self.wb.get_cell_value(self.s1, 'a2')
        a3_v = self.wb.get_cell_value(self.s1, 'a3')
        a4_v = self.wb.get_cell_value(self.s1, 'a4')
        b1_v = self.wb.get_cell_value(self.s1, 'b1')
        b2_v = self.wb.get_cell_value(self.s1, 'b2')
        b3_v = self.wb.get_cell_value(self.s1, 'b3')
        b4_v = self.wb.get_cell_value(self.s1, 'b4')
        self.assertIsInstance(a1_v, CellError)
        self.assertIsInstance(a2_v, CellError)
        self.assertIsInstance(a3_v, CellError)
        self.assertIsInstance(a4_v, CellError)
        self.assertIsInstance(b1_v, CellError)
        self.assertIsInstance(b2_v, CellError)
        self.assertIsInstance(b3_v, CellError)
        self.assertIsInstance(b4_v, CellError)
        self.assertEqual(a1_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertEqual(a2_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertEqual(a3_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertEqual(a4_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertEqual(b1_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertEqual(b2_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertEqual(b3_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertEqual(b4_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)

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

    def test_touch_loop(self):
        self.wb.set_cell_contents(self.s1, 'a1', '=b1')
        self.wb.set_cell_contents(self.s1, 'a2', '=a1')
        self.wb.set_cell_contents(self.s1, 'b1', '=a1')
        a1_v = self.wb.get_cell_value(self.s1, 'a1')
        a2_v = self.wb.get_cell_value(self.s1, 'a2')
        self.assertIsInstance(a1_v, CellError)
        self.assertEqual(a1_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertIsInstance(a2_v, CellError)
        self.assertEqual(a2_v.get_type(), CellErrorType.CIRCULAR_REFERENCE)

if __name__ == '__main__':
    unittest.main()
