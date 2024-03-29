# pylint: skip-file
import context
import unittest
import decimal
from sheets import *

class TestMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.wb = Workbook()
        _, self.s1 = self.wb.new_sheet()

    def test_if(self):
        self.wb.set_cell_contents(self.s1, 'a1', '= IF(a2, 1, 0)')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal())
        self.wb.set_cell_contents(self.s1, 'a2', 'True')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a3', '= a1')
        self.wb.set_cell_contents(self.s1, 'a1', '= IF(a2, a3, 0)')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.wb.set_cell_contents(self.s1, 'a2', 'False')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal())

    def test_iferror(self):
        self.wb.set_cell_contents(self.s1, 'a1', '= IFERROR(a2)')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal())
        self.wb.set_cell_contents(self.s1, 'a2', '#ERROR!')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, str)
        self.assertEqual(a1_val, "")
        self.wb.set_cell_contents(self.s1, 'a2', '1')
        self.wb.set_cell_contents(self.s1, 'a3', '0')
        self.wb.set_cell_contents(self.s1, 'a1', '= IFERROR(a2, a3)')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a2', '#ERROR!')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal())
        self.wb.set_cell_contents(self.s1, 'a2', '= a1')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.wb.set_cell_contents(self.s1, 'a2', '#ERROR!')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal())
        self.wb.set_cell_contents(self.s1, 'a3', '= a1')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.CIRCULAR_REFERENCE)

    def test_empty_iferror(self):
        self.wb.set_cell_contents(self.s1, 'a1', '= IFERROR()')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.TYPE_ERROR)

    def test_choose(self):
        self.wb.set_cell_contents(self.s1, 'a2', '1')
        self.wb.set_cell_contents(self.s1, 'a1', '= CHOOSE(a2, 1, 2)')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a2', '2')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal(2))
        self.wb.set_cell_contents(self.s1, 'a2', '1')
        self.wb.set_cell_contents(self.s1, 'a3', '= a1')
        self.wb.set_cell_contents(self.s1, 'a1', '= CHOOSE(a2, a3, 2)')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.wb.set_cell_contents(self.s1, 'a2', '2')
        self.wb.set_cell_contents(self.s1, 'a1', '= CHOOSE(a2, a3, 2)')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal(2))
        self.wb.set_cell_contents(self.s1, 'a2', '= a1')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.wb.set_cell_contents(self.s1, 'a2', '3')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.TYPE_ERROR)
        self.wb.set_cell_contents(self.s1, 'a2', 'Quickly')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.TYPE_ERROR)

    def test_choose_more(self):
        self.wb.set_cell_contents(self.s1, 'a1', '= CHOOSE(1, a1, 2)')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.wb.set_cell_contents(self.s1, 'a1', '= CHOOSE()')
        a1_val = self.wb.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.TYPE_ERROR)

if __name__ == '__main__':
    unittest.main()
