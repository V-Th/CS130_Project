# pylint: skip-file
import context
import unittest
import decimal
from sheets import *

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.workbook = Workbook()
        _, self.s1 = self.workbook.new_sheet()

    def test_booleans_1(self):
        self.workbook.set_cell_contents(self.s1, 'a1', 'true')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', 'false')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)

    def test_booleans_2(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '=true')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '=False')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)

    def test_comparison_1(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '=1 > 0')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)

    def test_comparison_2(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '=1 < 0')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)

    def test_comparison_3(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '=1 = 0')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)

    def test_comparison_4(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '=\"a\" < \"[\"')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)

    def test_comparison_5(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '=\"a\" < 42')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)

    def test_comparison_6(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '=True > 42')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)

if __name__ == '__main__':
    unittest.main()
