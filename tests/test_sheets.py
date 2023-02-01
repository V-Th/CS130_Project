import context
import unittest
import decimal
from sheets import *

class TestMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.wb = Workbook()
        _, self.s1 = self.wb.new_sheet()

    def test_del_sheet_1(self):
        self.wb.new_sheet("Sheet2")
        self.wb.set_cell_contents(self.s1, 'a1', '=sheet2!a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal())
        self.wb.del_sheet("sheet2")
        self.assertIsInstance(self.wb.get_cell_value(self.s1, 'a1'), CellError)
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1').get_type(), CellErrorType.BAD_REFERENCE)

    def test_del_sheet_2(self):
        self.wb.new_sheet("sheet2")
        self.wb.new_sheet("sheet3")
        self.wb.set_cell_contents("sheet3", 'a1', '=Sheet2!a1')
        self.wb.set_cell_contents("sheet2", 'a1', '=Sheet1!a1')
        self.wb.set_cell_contents("sheet1", 'a1', '=42')
        self.assertEqual(self.wb.get_cell_value("sheet1", 'a1'), decimal.Decimal(42))
        self.assertEqual(self.wb.get_cell_value("sheet2", 'a1'), decimal.Decimal(42))
        self.assertEqual(self.wb.get_cell_value("sheet3", 'a1'), decimal.Decimal(42))
        self.wb.del_sheet("SHEeT2")
        self.assertIsInstance(self.wb.get_cell_value("sheet3", 'a1'), CellError)
        self.assertEqual(self.wb.get_cell_value("sheet3", 'a1').get_type(), CellErrorType.BAD_REFERENCE)
        self.assertNotIsInstance(self.wb.get_cell_value("sheet1", 'a1'), CellError)

    def test_add_missing_sheet(self):
        self.wb.set_cell_contents(self.s1, 'a1', '=sheet2!a2')
        self.assertIsInstance(self.wb.get_cell_value(self.s1, 'a1'), CellError)
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1').get_type(), CellErrorType.BAD_REFERENCE)
        self.wb.new_sheet("Sheet2")
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal())

    def test_rename(self):
        _, _ = self.wb.new_sheet("Test")
        self.wb.set_cell_contents(self.s1, 'a1', '=Test!a1')
        self.wb.rename_sheet("test", 'Complete')
        self.assertEqual(self.wb.get_cell_contents(self.s1, 'a1'), '=Complete!a1')

    def test_sheet_quoting(self):
        _, _ = self.wb.new_sheet("Test")
        self.wb.set_cell_contents(self.s1, 'a1', '=\'Test\'!a1')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal())

    def test_unnecessary_quotes(self):
        _, _ = self.wb.new_sheet("Test")
        _, _ = self.wb.new_sheet("Rename")
        self.wb.set_cell_contents(self.s1, 'a1', '=\'Test\'!a1 + \'Test\'!a2 + Rename!a1')
        self.wb.rename_sheet("rename", 'Complete')
        self.assertEqual(self.wb.get_cell_contents(self.s1, 'a1'), '=Test!a1 + Test!a2 + Complete!a1')

if __name__ == '__main__':
    unittest.main()
