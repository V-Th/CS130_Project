import unittest
from unittest import TestCase
import decimal
from workbook import *
from cell_error import *

wb = Workbook()
(index1, name1) = wb.new_sheet()

class TestMethods():
    def test_cellref(self):
        wb.set_cell_contents(name1, 'a1', '=b1')
        value1 = wb.get_cell_value(name1, 'a1')
        assert value1 == decimal.Decimal()
        wb.set_cell_contents(name1, 'b1', '10')
        value2 = wb.get_cell_value(name1, 'b1')
        value3 = wb.get_cell_value(name1, 'a1')
        TestCase.assertEqual(value3, value2, 'a1 and b1 are not equal')
    
    def test_sheetref(self):
        (index2, name2) = wb.new_sheet()
        wb.set_cell_contents(name1, 'a1', '=Sheet1!b1')
        value = wb.get_cell_value(name1, 'a1')
        TestCase.assertEqual(value, decimal.Decimal(), 'cross sheet reference unsuccessful')
        wb.del_sheet(name2)
        TestCase.assertEqual(wb.num_sheets(), 1, 'Sheet2 not deleted')
        assert isinstance(wb.get_cell_value(name1, 'a1'), CellError)

    def test_sheetref_error(self):
        wb.set_cell_contents(name1, 'a1', '=Sheet1!b1')
        value = wb.get_cell_value(name1, 'a1')
        assert isinstance(value, CellError)
    
    def test_cycle_error(self):
        wb.set_cell_contents(name1, 'a1', '=b1')
        wb.set_cell_contents(name1, 'b1', '=c1')
        wb.set_cell_contents(name1, 'c1', '=a1')
        assert isinstance(wb.get_cell_value(name1, 'a1'), CellError)
        assert isinstance(wb.get_cell_value(name1, 'b1'), CellError)
        assert isinstance(wb.get_cell_value(name1, 'c1'), CellError)

    def test_zero_length(self):
        wb.set_cell_contents(name1, 'a1', '')
        assert wb.get_cell_contents(name1, 'a1') == None
        assert wb.get_cell_value(name1, 'a1') == None
    
    def test_extent1(self):
        wb.set_cell_contents(name1, 'z26', '10')
        TestCase.assertEqual(wb.get_sheet_extent(name1), (26,26), 'sheet extent incorrect')

    def test_extent2(self):
        (index2, name2) = wb.new_sheet()
        TestCase.assertEqual(wb.get_sheet_extent(name2), (0,0), 'default sheet extent incorrect')


if __name__ == '__main__':
    tm = TestMethods()
    tm.test_cellref()
    tm.test_sheetref()
    tm.test_sheetref_error()
    tm.test_cycle_error
    tm.test_zero_length
    tm.test_extent1()
    tm.test_extent2()
