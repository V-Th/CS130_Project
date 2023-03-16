# pylint: skip-file
import context
import unittest
import decimal
from sheets import *

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.wb = Workbook()
        _, self.s1 = self.wb.new_sheet()

    def test_errors(self):
        with self.assertRaises(KeyError):
            self.wb.sort_region('Bad Name', 'a1', 'a2', [1])
        with self.assertRaises(ValueError):
            self.wb.sort_region(self.s1, 'a1', 'b3', [1, 2, -1])
        with self.assertRaises(ValueError):
            self.wb.sort_region(self.s1, 'a1', 'b3', [1, 2, 0])
        with self.assertRaises(ValueError):
            self.wb.sort_region(self.s1, 'a1', 'b3', [])
        with self.assertRaises(ValueError):
            self.wb.sort_region(self.s1, 'a1', 'b3', [3])

    def test_sort_2_row_of_1(self):
        self.wb.set_cell_contents(self.s1, 'a1', '2')
        self.wb.set_cell_contents(self.s1, 'a2', '1')
        self.wb.sort_region(self.s1, 'a1', 'a2', [1])
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        a2_val = self.wb.get_cell_value(self.s1, 'a2')
        self.assertEqual(a1_val, decimal.Decimal(1))
        self.assertEqual(a2_val, decimal.Decimal(2))

    def test_sort_3_row_of_1(self):
        self.wb.set_cell_contents(self.s1, 'a1', '2')
        self.wb.set_cell_contents(self.s1, 'a2', '3')
        self.wb.set_cell_contents(self.s1, 'a3', '1')
        self.wb.sort_region(self.s1, 'a3', 'a1', [1])
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        a2_val = self.wb.get_cell_value(self.s1, 'a2')
        a3_val = self.wb.get_cell_value(self.s1, 'a3')
        self.assertEqual(a1_val, decimal.Decimal(1))
        self.assertEqual(a2_val, decimal.Decimal(2))
        self.assertEqual(a3_val, decimal.Decimal(3))

    def test_sort_3_row_of_2(self):
        self.wb.set_cell_contents(self.s1, 'a1', '2')
        self.wb.set_cell_contents(self.s1, 'a2', '3')
        self.wb.set_cell_contents(self.s1, 'a3', '1')
        self.wb.set_cell_contents(self.s1, 'b1', '= a1')
        self.wb.set_cell_contents(self.s1, 'b2', '\'hi')
        self.wb.set_cell_contents(self.s1, 'b3', 'True')
        self.wb.sort_region(self.s1, 'a1', 'b3', [1, 2])
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        a2_val = self.wb.get_cell_value(self.s1, 'a2')
        a3_val = self.wb.get_cell_value(self.s1, 'a3')
        b1_val = self.wb.get_cell_value(self.s1, 'b1')
        b2_val = self.wb.get_cell_value(self.s1, 'b2')
        b3_val = self.wb.get_cell_value(self.s1, 'b3')
        self.assertEqual(a1_val, decimal.Decimal(1))
        self.assertEqual(a2_val, decimal.Decimal(2))
        self.assertEqual(a3_val, decimal.Decimal(3))
        self.assertEqual(b1_val, True)
        self.assertEqual(b2_val, decimal.Decimal(2))
        self.assertEqual(b3_val, 'hi')

    def test_sort_3_row_of_2_2(self):
        self.wb.set_cell_contents(self.s1, 'a1', '2')
        self.wb.set_cell_contents(self.s1, 'a2', '3')
        self.wb.set_cell_contents(self.s1, 'a3', '1')
        self.wb.set_cell_contents(self.s1, 'b1', '= a1')
        self.wb.set_cell_contents(self.s1, 'b2', '\'hi')
        self.wb.set_cell_contents(self.s1, 'b3', 'True')
        self.wb.sort_region(self.s1, 'a1', 'b3', [2, 1])
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        a2_val = self.wb.get_cell_value(self.s1, 'a2')
        a3_val = self.wb.get_cell_value(self.s1, 'a3')
        b1_val = self.wb.get_cell_value(self.s1, 'b1')
        b2_val = self.wb.get_cell_value(self.s1, 'b2')
        b3_val = self.wb.get_cell_value(self.s1, 'b3')
        self.assertEqual(a1_val, decimal.Decimal(2))
        self.assertEqual(a2_val, decimal.Decimal(3))
        self.assertEqual(a3_val, decimal.Decimal(1))
        self.assertEqual(b1_val, decimal.Decimal(2))
        self.assertEqual(b2_val, 'hi')
        self.assertEqual(b3_val, True)
    
    def test_sort_3_row_of_3(self):
        self.wb.set_cell_contents(self.s1, 'a1', '2')
        self.wb.set_cell_contents(self.s1, 'a2', '3')
        self.wb.set_cell_contents(self.s1, 'a3', '1')
        self.wb.set_cell_contents(self.s1, 'b1', '= a1')
        self.wb.set_cell_contents(self.s1, 'b2', '\'hi')
        self.wb.set_cell_contents(self.s1, 'b3', 'True')
        self.wb.set_cell_contents(self.s1, 'c1', '')
        self.wb.set_cell_contents(self.s1, 'c2', '\'bye')
        self.wb.set_cell_contents(self.s1, 'c3', '')
        self.wb.sort_region(self.s1, 'a1', 'c3', [3, 2, 1])
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        a2_val = self.wb.get_cell_value(self.s1, 'a2')
        a3_val = self.wb.get_cell_value(self.s1, 'a3')
        b1_val = self.wb.get_cell_value(self.s1, 'b1')
        b2_val = self.wb.get_cell_value(self.s1, 'b2')
        b3_val = self.wb.get_cell_value(self.s1, 'b3')
        c1_val = self.wb.get_cell_value(self.s1, 'c1')
        c2_val = self.wb.get_cell_value(self.s1, 'c2')
        c3_val = self.wb.get_cell_value(self.s1, 'c3')
        self.assertEqual(a1_val, decimal.Decimal(2))
        self.assertEqual(a2_val, decimal.Decimal(1))
        self.assertEqual(a3_val, decimal.Decimal(3))
        self.assertEqual(b1_val, decimal.Decimal(2))
        self.assertEqual(b2_val, True)
        self.assertEqual(b3_val, 'hi')
        self.assertIsNone(c1_val)
        self.assertIsNone(c2_val)
        self.assertEqual(c3_val, 'bye')

    def test_sort_3_row_of_3_R(self):
        self.wb.set_cell_contents(self.s1, 'a1', '2')
        self.wb.set_cell_contents(self.s1, 'a2', '3')
        self.wb.set_cell_contents(self.s1, 'a3', '1')
        self.wb.set_cell_contents(self.s1, 'b1', '= a1')
        self.wb.set_cell_contents(self.s1, 'b2', '\'hi')
        self.wb.set_cell_contents(self.s1, 'b3', 'True')
        self.wb.set_cell_contents(self.s1, 'c1', '')
        self.wb.set_cell_contents(self.s1, 'c2', '\'bye')
        self.wb.set_cell_contents(self.s1, 'c3', '')
        self.wb.sort_region(self.s1, 'a1', 'c3', [2, 1, 3])
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        a2_val = self.wb.get_cell_value(self.s1, 'a2')
        a3_val = self.wb.get_cell_value(self.s1, 'a3')
        b1_val = self.wb.get_cell_value(self.s1, 'b1')
        b2_val = self.wb.get_cell_value(self.s1, 'b2')
        b3_val = self.wb.get_cell_value(self.s1, 'b3')
        c1_val = self.wb.get_cell_value(self.s1, 'c1')
        c2_val = self.wb.get_cell_value(self.s1, 'c2')
        c3_val = self.wb.get_cell_value(self.s1, 'c3')
        self.assertEqual(a1_val, decimal.Decimal(2))
        self.assertEqual(a2_val, decimal.Decimal(3))
        self.assertEqual(a3_val, decimal.Decimal(1))
        self.assertEqual(b1_val, decimal.Decimal(2))
        self.assertEqual(b2_val, 'hi')
        self.assertEqual(b3_val, True)
        self.assertIsNone(c1_val)
        self.assertEqual(c2_val, 'bye')
        self.assertIsNone(c3_val)

    def test_sort_shift_cells(self):
        self.wb.set_cell_contents(self.s1, 'a1', '= b1')
        self.wb.set_cell_contents(self.s1, 'a2', '= b2')
        self.wb.set_cell_contents(self.s1, 'a3', '= b3')
        self.wb.set_cell_contents(self.s1, 'b1', '')
        self.wb.set_cell_contents(self.s1, 'b2', '\'Almost Done')
        self.wb.set_cell_contents(self.s1, 'b3', '49')
        self.wb.sort_region(self.s1, 'a1', 'a3', [1])
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        a2_val = self.wb.get_cell_value(self.s1, 'a2')
        a3_val = self.wb.get_cell_value(self.s1, 'a3')
        # Although the cells sort, the shift does not change their value
        self.assertEqual(a1_val, decimal.Decimal())
        self.assertEqual(a2_val, 'Almost Done')
        self.assertEqual(a3_val, decimal.Decimal(49))

    def test_sort_no_shift_cells(self):
        self.wb.set_cell_contents(self.s1, 'a1', '= $b$1')
        self.wb.set_cell_contents(self.s1, 'a2', '= $b$2')
        self.wb.set_cell_contents(self.s1, 'a3', '= $b$3')
        self.wb.set_cell_contents(self.s1, 'b1', '')
        self.wb.set_cell_contents(self.s1, 'b2', '\'Almost Done')
        self.wb.set_cell_contents(self.s1, 'b3', '49')
        self.wb.sort_region(self.s1, 'a1', 'a3', [1])
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        a2_val = self.wb.get_cell_value(self.s1, 'a2')
        a3_val = self.wb.get_cell_value(self.s1, 'a3')
        self.assertEqual(a1_val, decimal.Decimal())
        self.assertEqual(a2_val, decimal.Decimal(49))
        self.assertEqual(a3_val, 'Almost Done')

    def test_sort_shift_out(self):
        self.wb.set_cell_contents(self.s1, 'a1', '= b2')
        self.wb.set_cell_contents(self.s1, 'a2', '= b1')
        self.wb.set_cell_contents(self.s1, 'b1', '1')
        self.wb.set_cell_contents(self.s1, 'b2', '\'Almost Done')
        self.wb.sort_region(self.s1, 'a1', 'a2', [1])
        # a2 moves up shift its content out of range
        # a1 moves down so it becomes 0 as b3 is its content
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        a2_val = self.wb.get_cell_value(self.s1, 'a2')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.BAD_REFERENCE)
        self.assertEqual(a2_val, decimal.Decimal())


if __name__ == '__main__':
    unittest.main()
