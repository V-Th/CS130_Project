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


if __name__ == '__main__':
    unittest.main()
