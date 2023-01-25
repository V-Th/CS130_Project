import context
import unittest
from unittest import TestCase
import decimal
from sheets import *

wb = Workbook()
(index1, name1) = wb.new_sheet()

class TestWorkbook(unittest.TestCase):

    # If we have a cell A1 which is set to the value of D4, then the extent of the sheet is (1, 1) 
    # if D4 = None even though it is part of the formula for A1.
    def test_extent_1(self):
        wb.set_cell_contents(name1, 'a1', '=d4')
        assert wb.get_sheet_extent(name1) == (1,1)
        wb.set_cell_contents(name1, 'd1', '10')
        assert wb.get_sheet_extent(name1) == (4,4)
    
    # A sheet's extent should shrink as the maximal cell's contents are cleared.
    def test_extent_2(self):
        extent = wb.get_sheet_extent(name1)
        wb.set_cell_contents(name1, 'e5', '10')
        assert wb.get_sheet_extent(name1) == (5,5)
        wb.set_cell_contents(name1, 'e5', 'None')
        assert wb.get_sheet_extent(name1) == extent
    
    def test_extent_3(self):
        extent = wb.get_sheet_extent(name1)
        wb.set_cell_contents(name1, 'a1', '10')
        wb.set_cell_contents(name1, 'b1', '20')
        wb.set_cell_contents(name1, 'c1', '30')
        wb.set_cell_contents(name1, 'a1', '')
        wb.set_cell_contents(name1, 'b1', '')
        wb.set_cell_contents(name1, 'c1', '')
        assert wb.get_sheet_extent(name1) == extent

    # The Workbook.list_sheets() API should reflect delete operations against the workbook.
    def test_listsheets_1(self):
        num_sheets = wb.num_sheets()
        sheet_list = wb.list_sheets()
        sheet_list.append("test_listsheets_1")
        assert len(wb.list_sheets()) == num_sheets
        assert "test_listsheets_1" not in wb.list_sheets()
    
    # The Workbook.list_sheets() API should reflect delete operations against the workbook.
    def test_listsheets_2(self):
        (index2, name2) = wb.new_sheet()
        (index3, name3) = wb.new_sheet()
        wb.del_sheet(name2)
        wb.del_sheet(name3)
        assert name2 not in wb.list_sheets()
        assert name3 not in wb.list_sheets()
    
    # The Workbook.list_sheets() API should reflect delete and then new operations 
    # against the workbook.
    def test_listsheets_3(self):
        (index2, name2) = wb.new_sheet()
        wb.del_sheet(name2)
        assert name2 not in wb.list_sheets()
        (index3, name3) = wb.new_sheet()
        assert name3 in wb.list_sheets()

    # Add a sheet with double-quotes in the name to ensure an error is raised.
    def test_newsheet_1(self):
        with TestCase.assertRaises(ValueError):
            wb.new_sheet('\'sheet2\'') 
    
    # Add a sheet with a zero-length string to ensure an error is raised.
    def test_newsheet_2(self):
        with TestCase.assertRaises(ValueError):
            wb.new_sheet('') 

    # Add a few named sheets to a workbook
    def test_newsheet_3(self):
        num_sheets = wb.num_sheets()
        (index2, name2) = wb.new_sheet("sheet2") 
        (index3, name3) = wb.new_sheet("sheet3") 
        (index4, name4) = wb.new_sheet("sheet4") 
        assert wb.num_sheets() == num_sheets + 3
        assert name2 in wb.list_sheets()
        assert name3 in wb.list_sheets()
        assert name4 in wb.list_sheets()
    
    # Add a mix of named and unnamed sheets to a workbook
    def test_newsheet_4(self):
        num_sheets = wb.num_sheets()
        (index2, name2) = wb.new_sheet("new sheet") 
        (index3, name3) = wb.new_sheet() 
        (index4, name4) = wb.new_sheet() 
        (index5, name5) = wb.new_sheet("another new sheet") 
        assert wb.num_sheets() == num_sheets + 4
        assert name2 in wb.list_sheets()
        assert name3 in wb.list_sheets()
        assert name4 in wb.list_sheets()
        assert name5 in wb.list_sheets()
    
    # Add a mix of named and unnamed sheets to a workbook whose names overlap
    def test_newsheet_5(self):
        num_sheets = wb.num_sheets()
        (index2, name2) = wb.new_sheet("new sheet") 
        (index3, name3) = wb.new_sheet() 
        (index4, name4) = wb.new_sheet("new sheet") 
    
    # Add a mix of named and unnamed sheets to a workbook whose names overlap
    def test_newsheet_6(self):
        num_sheets = wb.num_sheets()
        (index2, name2) = wb.new_sheet() 
        assert name2 == 'Sheet' + (num_sheets+1)
        assert wb.num_sheets() == num_sheets + 1
        (index3, name3) = wb.new_sheet() 
        assert name3 == 'Sheet' + (num_sheets+2)
        assert wb.num_sheets() == num_sheets + 2
        (index4, name4) = wb.new_sheet() 
        assert name3 == 'Sheet' + (num_sheets+3)
        assert wb.num_sheets() == num_sheets + 3

    # Add a sheet with a whitespace-only string to ensure an error is raised.
    def test_newsheet_7(self):
        with TestCase.assertRaises(ValueError):
            wb.new_sheet('  ')

    # Construction of a new empty workbook with no spreadsheets.
    def test_workbook(self):
        wb2 = Workbook()
        assert wb2.num_sheets() == 0
        assert wb2.list_sheets() == []
    
    # Verifies that setting a cell to an error-value string will cause the cell to take on 
    # the corresponding error value.
    def test_errorstring(self):
        wb.set_cell_contents(name1, 'a1', '#ERROR!')
        wb.set_cell_contents(name1, 'b1', '#CIRCEF!')
        wb.set_cell_contents(name1, 'c1', '#REF!')
        wb.set_cell_contents(name1, 'd1', '#NAME!')
        wb.set_cell_contents(name1, 'e1', '#VALUE!')
        wb.set_cell_contents(name1, 'f1', '#DIV/0!')
        assert isinstance(wb.get_cell_value(name1, 'a1'), sheets.CellError)
        assert isinstance(wb.get_cell_value(name1, 'b1'), sheets.CellError)
        assert isinstance(wb.get_cell_value(name1, 'c1'), sheets.CellError)
        assert isinstance(wb.get_cell_value(name1, 'd1'), sheets.CellError)
        assert isinstance(wb.get_cell_value(name1, 'e1'), sheets.CellError)
        assert isinstance(wb.get_cell_value(name1, 'f1'), sheets.CellError)


if __name__ == '__main__':
    tw = TestWorkbook()
    tw.test_extent_1()
    tw.test_extent_2()
    tw.test_extent_3()
    tw.test_listsheets_1()
    tw.test_listsheets_2()
    tw.test_listsheets_3()
    tw.test_newsheet_1()
    tw.test_newsheet_2()
    tw.test_newsheet_3()
    tw.test_newsheet_4()
    tw.test_newsheet_5()
    tw.test_newsheet_6()
    tw.test_newsheet_7()
    tw.test_workbook()
    tw.test_errorstring()