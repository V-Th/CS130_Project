import context
import unittest
from unittest import TestCase
import decimal
from sheets import *

class TestWorkbook(unittest.TestCase):

    def setUp(self) -> None:
        self.wb = Workbook()
        (_, self.name1) = self.wb.new_sheet()

    # If we have a cell A1 which is set to the value of D4, then the extent of the sheet is (1, 1) 
    # if D4 = None even though it is part of the formula for A1.
    def test_extent_1(self):
        self.wb.set_cell_contents(self.name1, 'a1', '=d4')
        self.assertEqual(self.wb.get_sheet_extent(self.name1), (1,1))
        self.wb.set_cell_contents(self.name1, 'd1', '10')
        self.assertEqual(self.wb.get_sheet_extent(self.name1), (4,4))
    
    # A sheet's extent should shrink as the maximal cell's contents are cleared.
    def test_extent_2(self):
        extent = self.wb.get_sheet_extent(self.name1)
        self.wb.set_cell_contents(self.name1, 'e5', '10')
        self.assertEqual(self.wb.get_sheet_extent(self.name1), (5,5))
        self.wb.set_cell_contents(self.name1, 'e5', 'None')
        self.assertEqual(self.wb.get_sheet_extent(self.name1), extent)
    
    def test_extent_3(self):
        extent = self.wb.get_sheet_extent(self.name1)
        self.wb.set_cell_contents(self.name1, 'a1', '10')
        self.wb.set_cell_contents(self.name1, 'b1', '20')
        self.wb.set_cell_contents(self.name1, 'c1', '30')
        self.wb.set_cell_contents(self.name1, 'a1', '')
        self.wb.set_cell_contents(self.name1, 'b1', '')
        self.wb.set_cell_contents(self.name1, 'c1', '')
        self.assertEqual(self.wb.get_sheet_extent(self.name1), extent)

    # The Workbook.list_sheets() API should reflect delete operations against the workbook.
    def test_listsheets_1(self):
        num_sheets = self.wb.num_sheets()
        sheet_list = self.wb.list_sheets()
        sheet_list.append("test_listsheets_1")
        self.assertEqual(len(self.wb.list_sheets()), num_sheets)
        self.assertTrue("test_listsheets_1" not in self.wb.list_sheets())
    
    # The Workbook.list_sheets() API should reflect delete operations against the workbook.
    def test_listsheets_2(self):
        (_, name2) = self.wb.new_sheet()
        (_, name3) = self.wb.new_sheet()
        self.wb.del_sheet(name2)
        self.wb.del_sheet(name3)
        self.assertTrue(name2 not in self.wb.list_sheets())
        self.assertTrue(name3 not in self.wb.list_sheets())
    
    # The Workbook.list_sheets() API should reflect delete and then new operations 
    # against the workbook.
    def test_listsheets_3(self):
        (_, name2) = self.wb.new_sheet()
        self.wb.del_sheet(name2)
        self.assertTrue(name2 not in self.wb.list_sheets())
        (_, name3) = self.wb.new_sheet()
        self.assertTrue(name3 in self.wb.list_sheets())

    # Add a sheet with double-quotes in the name to ensure an error is raised.
    def test_newsheet_1(self):
        with self.assertRaises(ValueError):
            self.wb.new_sheet('\'sheet2\'') 
    
    # Add a sheet with a zero-length string to ensure an error is raised.
    def test_newsheet_2(self):
        with self.assertRaises(ValueError):
            self.wb.new_sheet('') 

    # Add a few named sheets to a workbook
    def test_newsheet_3(self):
        num_sheets = self.wb.num_sheets()
        (_, name2) = self.wb.new_sheet("sheet2") 
        (_, name3) = self.wb.new_sheet("sheet3") 
        (_, name4) = self.wb.new_sheet("sheet4") 
        self.assertEqual(self.wb.num_sheets(), num_sheets + 3)
        self.assertTrue(name2 in self.wb.list_sheets())
        self.assertTrue(name3 in self.wb.list_sheets())
        self.assertTrue(name4 in self.wb.list_sheets())
    
    # Add a mix of named and unnamed sheets to a workbook
    def test_newsheet_4(self):
        num_sheets = self.wb.num_sheets()
        (_, name2) = self.wb.new_sheet("new sheet") 
        (_, name3) = self.wb.new_sheet() 
        (_, name4) = self.wb.new_sheet() 
        (_, name5) = self.wb.new_sheet("another new sheet") 
        self.assertEqual(self.wb.num_sheets(), num_sheets + 4)
        self.assertTrue(name2 in self.wb.list_sheets())
        self.assertTrue(name3 in self.wb.list_sheets())
        self.assertTrue(name4 in self.wb.list_sheets())
        self.assertTrue(name5 in self.wb.list_sheets())
    
    # Add a mix of named and unnamed sheets to a workbook whose names overlap
    def test_newsheet_5(self):
        with self.assertRaises(ValueError):
            (_, _) = self.wb.new_sheet("new sheet")
            (_, _) = self.wb.new_sheet("new sheet") 
    
    # Add a mix of named and unnamed sheets to a workbook whose names overlap
    def test_newsheet_6(self):
        num_sheets = self.wb.num_sheets()
        (_, name2) = self.wb.new_sheet() 
        self.assertEqual(name2, 'Sheet' + str(num_sheets+1))
        self.assertEqual(self.wb.num_sheets(), num_sheets + 1)
        (_, name3) = self.wb.new_sheet() 
        self.assertEqual(name3, 'Sheet' + str(num_sheets+2))
        self.assertEqual(self.wb.num_sheets(), num_sheets + 2)
        (_, name4) = self.wb.new_sheet() 
        self.assertEqual(name4, 'Sheet' + str(num_sheets+3))
        self.assertEqual(self.wb.num_sheets(), num_sheets + 3)

    # Add a sheet with a whitespace-only string to ensure an error is raised.
    def test_newsheet_7(self):
        with self.assertRaises(ValueError):
            self.wb.new_sheet('  ')

    # Construction of a new empty workbook with no spreadsheets.
    def test_workbook(self):
        wb2 = Workbook()
        self.assertEqual(wb2.num_sheets(), 0)
        self.assertFalse(wb2.list_sheets())
    
    # Verifies that setting a cell to an error-value string will cause the cell to take on 
    # the corresponding error value.
    def test_errorstring(self):
        self.wb.set_cell_contents(self.name1, 'a1', '#ERROR!')
        self.wb.set_cell_contents(self.name1, 'b1', '#CIRCEF!')
        self.wb.set_cell_contents(self.name1, 'c1', '#REF!')
        self.wb.set_cell_contents(self.name1, 'd1', '#NAME!')
        self.wb.set_cell_contents(self.name1, 'e1', '#VALUE!')
        self.wb.set_cell_contents(self.name1, 'f1', '#DIV/0!')
        self.assertEqual(self.wb.get_cell_value(self.name1, 'a1'), CellError)
        self.assertEqual(self.wb.get_cell_value(self.name1, 'b1'), CellError)
        self.assertEqual(self.wb.get_cell_value(self.name1, 'c1'), CellError)
        self.assertEqual(self.wb.get_cell_value(self.name1, 'd1'), CellError)
        self.assertEqual(self.wb.get_cell_value(self.name1, 'e1'), CellError)
        self.assertEqual(self.wb.get_cell_value(self.name1, 'f1'), CellError)


if __name__ == '__main__':
    unittest.main()
