import context
import unittest
import decimal
from sheets import *

class TestMethods(unittest.TestCase):
    def setUp(self) -> None:
        self.wb = Workbook()
        _, self.s1 = self.wb.new_sheet()

    def test_quoted_string_leading_whitespace(self):
        '''
        Test that the leading white space in a quoted string value is preserved
        '''
        self.wb.set_cell_contents(self.s1, 'a1', '\'   hi')
        self.wb.set_cell_contents(self.s1, 'a2', '=\"   hi\"')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), '   hi')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a2'), '   hi')
        
    def test_error_value_str(self):
        '''
        Test that setting a cell to an error-value string will cause the value
        to take the corresponding error
        '''
        self.wb.set_cell_contents(self.s1, 'a1', '#ERROR!')
        self.wb.set_cell_contents(self.s1, 'a2', '#CIRCREF!')
        self.wb.set_cell_contents(self.s1, 'a3', '#REF!')
        self.wb.set_cell_contents(self.s1, 'a4', '#NAME?')
        self.wb.set_cell_contents(self.s1, 'a5', '#VALUE!')
        self.wb.set_cell_contents(self.s1, 'a6', '#DIV/0!')
        a1_v = self.wb.get_cell_value(self.s1, 'a1')
        a2_v = self.wb.get_cell_value(self.s1, 'a2')
        a3_v = self.wb.get_cell_value(self.s1, 'a3')
        a4_v = self.wb.get_cell_value(self.s1, 'a4')
        a5_v = self.wb.get_cell_value(self.s1, 'a5')
        a6_v = self.wb.get_cell_value(self.s1, 'a6')
        self.assertIsInstance(a1_v, CellError)
        self.assertIsInstance(a2_v, CellError)
        self.assertIsInstance(a3_v, CellError)
        self.assertIsInstance(a4_v, CellError)
        self.assertIsInstance(a5_v, CellError)
        self.assertIsInstance(a6_v, CellError)
        self.assertEqual(a1_v.get_type(), CellErrorType('#ERROR!'))
        self.assertEqual(a2_v.get_type(), CellErrorType('#CIRCREF!'))
        self.assertEqual(a3_v.get_type(), CellErrorType('#REF!'))
        self.assertEqual(a4_v.get_type(), CellErrorType('#NAME?'))
        self.assertEqual(a5_v.get_type(), CellErrorType('#VALUE!'))
        self.assertEqual(a6_v.get_type(), CellErrorType('#DIV/0!'))

    def test_add_cell_number(self):
        '''
        Test placing various whitespaces in subtracting cell with number
        '''
        self.wb.set_cell_contents(self.s1, 'a1', '= a2 + 1')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '= a2     + 1')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '= a2 + 1      ')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '=     a2 + 1')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '    = a2 + 1')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))

    def test_add_number_cell(self):
        '''
        Test placing various whitespaces in subtracting number with cell
        '''
        self.wb.set_cell_contents(self.s1, 'a2', '1')
        self.wb.set_cell_contents(self.s1, 'a1', '= 0 + a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '= 0     + a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '= 0 + a2      ')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '=     0 + a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '    = 0 + a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))

    def test_subtract_cell_number(self):
        '''
        Test placing various whitespaces in subtracting cell with number
        '''
        self.wb.set_cell_contents(self.s1, 'a1', '= a2 - 1')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(-1))
        self.wb.set_cell_contents(self.s1, 'a1', '= a2     - 1')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(-1))
        self.wb.set_cell_contents(self.s1, 'a1', '= a2 - 1      ')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(-1))
        self.wb.set_cell_contents(self.s1, 'a1', '=     a2 - 1')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(-1))
        self.wb.set_cell_contents(self.s1, 'a1', '    = a2 - 1')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(-1))

    def test_subtract_number_cell(self):
        '''
        Test placing various whitespaces in subtracting number with cell
        '''
        self.wb.set_cell_contents(self.s1, 'a1', '= 1 - a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '= 1     - a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '= 1 - a2      ')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '=     1 - a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))
        self.wb.set_cell_contents(self.s1, 'a1', '    = 1 - a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(1))

    def test_multiply_cell_number(self):
        '''
        Test placing various whitespaces in multiplying cell with number
        '''
        self.wb.set_cell_contents(self.s1, 'a2', '21')
        self.wb.set_cell_contents(self.s1, 'a1', '= a2 * 2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(42))
        self.wb.set_cell_contents(self.s1, 'a1', '= a2     * 2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(42))
        self.wb.set_cell_contents(self.s1, 'a1', '= a2 * 2      ')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(42))
        self.wb.set_cell_contents(self.s1, 'a1', '=     a2 * 2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(42))
        self.wb.set_cell_contents(self.s1, 'a1', '    = a2 * 2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(42))

    def test_multiply_number_cell(self):
        '''
        Test placing various whitespaces in multiplying number with cell
        '''
        self.wb.set_cell_contents(self.s1, 'a2', '21')
        self.wb.set_cell_contents(self.s1, 'a1', '= a2 * 2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(42))
        self.wb.set_cell_contents(self.s1, 'a1', '= 2     * a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(42))
        self.wb.set_cell_contents(self.s1, 'a1', '= 2 * a2      ')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(42))
        self.wb.set_cell_contents(self.s1, 'a1', '=     2 * a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(42))
        self.wb.set_cell_contents(self.s1, 'a1', '    = 2 * a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), decimal.Decimal(42))

    def test_concat_numbers_string(self):
        '''
        Test string concatenation with numbers
        '''
        self.wb.set_cell_contents(self.s1, 'a1', '=\"high\"&5')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "high5")
        self.wb.set_cell_contents(self.s1, 'a1', '=\"high\"&5.00')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "high5")

    def test_concat_cells_string(self):
        '''
        Test string concatenation with cells
        '''
        self.wb.set_cell_contents(self.s1, 'a1', '=a2&a3')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "")
        self.wb.set_cell_contents(self.s1, 'a2', '\'Hello')
        self.wb.set_cell_contents(self.s1, 'a1', '= a2 & \" world\"')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "Hello world")
        self.wb.set_cell_contents(self.s1, 'a1', '= a2 &    \" world\"')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "Hello world")
        self.wb.set_cell_contents(self.s1, 'a1', '= a2    & \" world\"')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "Hello world")
        self.wb.set_cell_contents(self.s1, 'a1', '=    a2 & \" world\"')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "Hello world")
        self.wb.set_cell_contents(self.s1, 'a1', '   = a2 & \" world\"')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "Hello world")
        self.wb.set_cell_contents(self.s1, 'a2', '\' world')
        self.wb.set_cell_contents(self.s1, 'a1', '= \"Hello\" & a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "Hello world")
        self.wb.set_cell_contents(self.s1, 'a1', '= \"Hello\" &    a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "Hello world")
        self.wb.set_cell_contents(self.s1, 'a1', '= \"Hello\"    & a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "Hello world")
        self.wb.set_cell_contents(self.s1, 'a1', '=    \"Hello\" & a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "Hello world")
        self.wb.set_cell_contents(self.s1, 'a1', '   = \"Hello\" & a2')
        self.assertEqual(self.wb.get_cell_value(self.s1, 'a1'), "Hello world")

    def test_error_arithmetic(self):
        '''
        Test whether errors are properly passed
        '''
        for errortype in CellErrorType:
            self.wb.set_cell_contents(self.s1, 'a1', '='+errortype.value)
            self.assertEqual(self.wb.get_cell_value(self.s1, 'a1').get_type(), errortype)
            self.wb.set_cell_contents(self.s1, 'a1', '=-'+errortype.value)
            self.assertEqual(self.wb.get_cell_value(self.s1, 'a1').get_type(), errortype)
            self.wb.set_cell_contents(self.s1, 'a1', '=4+'+errortype.value)
            self.assertEqual(self.wb.get_cell_value(self.s1, 'a1').get_type(), errortype)
            self.wb.set_cell_contents(self.s1, 'a1', '=4-'+errortype.value)
            self.assertEqual(self.wb.get_cell_value(self.s1, 'a1').get_type(), errortype)
            self.wb.set_cell_contents(self.s1, 'a1', '=4*'+errortype.value)
            self.assertEqual(self.wb.get_cell_value(self.s1, 'a1').get_type(), errortype)
            self.wb.set_cell_contents(self.s1, 'a1', '=4/'+errortype.value)
            self.assertEqual(self.wb.get_cell_value(self.s1, 'a1').get_type(), errortype)
            self.wb.set_cell_contents(self.s1, 'a1', '=('+errortype.value+')')
            self.assertEqual(self.wb.get_cell_value(self.s1, 'a1').get_type(), errortype)

if __name__ == '__main__':
    unittest.main()
