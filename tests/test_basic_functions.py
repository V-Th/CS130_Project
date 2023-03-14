# pylint: skip-file
import context
import unittest
import decimal
import sheets

# Make a new empty workbook 
wb = sheets.Workbook()
(index, name) = wb.new_sheet()

class TestWorkbook(unittest.TestCase):
    # create cells
    # numbers
    def test_num_cell_1(self): 
        wb.set_cell_contents(name, 'a1', '10')
        self.assertEqual(wb.get_cell_value(name, 'a1'), 10)
    
    def test_num_cell_2(self): 
        wb.set_cell_contents(name, 'b1', '1234567890')
        self.assertEqual(wb.get_cell_value(name, 'b1'), 1234567890)
        
    def test_num_cell_3(self): 
        wb.set_cell_contents(name, 'c1', '=-1234567890')
        self.assertEqual(wb.get_cell_value(name, 'c1'), -1234567890)
    
    def test_num_cell_4(self): 
        wb.set_cell_contents(name, 'a1', '   10')
        self.assertEqual(wb.get_cell_value(name, 'a1'), 10)

    # strings 
    def test_string_cell_1(self): 
        wb.set_cell_contents(name, 'a1', "one two three")
        self.assertEqual(wb.get_cell_value(name, 'a1'), "one two three")

    def test_string_cell_2(self): 
        wb.set_cell_contents(name, 'b1', " ")
        self.assertEqual(wb.get_cell_value(name, 'b1'), None)

    def test_string_cell_3(self): 
        wb.set_cell_contents(name, 'c1', '   one   ')
        self.assertEqual(wb.get_cell_value(name, 'c1'), 'one')

    # test functions
    # add_expr
    def test_add_formula_1(self): 
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'b1', '20')
        wb.set_cell_contents(name, 'c1', '=a1+b1')  # 30
        self.assertEqual(wb.get_cell_value(name, 'c1'), 30)
    
    def test_add_formula_2(self): 
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'b1', '20')
        wb.set_cell_contents(name, 'd1', '=a1-b1')  # -10
        self.assertEqual(wb.get_cell_value(name, 'd1'), -10)
    
    def test_add_formula_3(self): 
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'b1', '20')
        wb.set_cell_contents(name, 'e1', '=(a1+b1)')  # 30
        self.assertEqual(wb.get_cell_value(name, 'e1'), 30)
    
    def test_add_formula_4(self): 
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'b1', '20')
        wb.set_cell_contents(name, 'f1', '=(b1-a1+b1)+(-b1-a1-a1)+b1')  # 10
        self.assertEqual(wb.get_cell_value(name, 'f1'), 10)
        
    # concat_expr
    def test_concat_formula_1(self): 
        wb.set_cell_contents(name, 'a1', "one")
        wb.set_cell_contents(name, 'b1', "two")
        wb.set_cell_contents(name, 'c1', "=a1&b1") 
        self.assertEqual(wb.get_cell_value(name, 'c1'), "onetwo")
    
    def test_concat_formula_2(self): 
        wb.set_cell_contents(name, 'a1', "one")
        wb.set_cell_contents(name, 'b1', "two")
        wb.set_cell_contents(name, 'd1', "=a1&\" \"&b1") 
        self.assertEqual(wb.get_cell_value(name, 'd1'), "one two")
    
    def test_concat_formula_3(self): 
        wb.set_cell_contents(name, 'e1', "=7&9") 
        self.assertEqual(wb.get_cell_value(name, 'e1'), "79")
    
    # mul_expr (multiply)
    def test_mul_formula_1(self): 
        wb.set_cell_contents(name, 'a1', '50')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'c1', '=a1*b1')  # 500
        self.assertEqual(wb.get_cell_value(name, 'c1'), decimal.Decimal(500))
    
    def test_mul_formula_2(self): 
        wb.set_cell_contents(name, 'a1', '50')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'd1', '=a1*b1*10000')  # 5000000
        self.assertEqual(wb.get_cell_value(name, 'd1'), decimal.Decimal(5000000))
    
    def test_mul_formula_3(self): 
        wb.set_cell_contents(name, 'a1', '50')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'e1', '=a1*b1*-1')  # -500
        self.assertEqual(wb.get_cell_value(name, 'e1'), decimal.Decimal(-500))
    
    # mul_expr (divide)
    def test_div_formula_1(self): 
        wb.set_cell_contents(name, 'a1', '50')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'c1', '=a1/b1')  # 5
        self.assertEqual(wb.get_cell_value(name, 'c1'), decimal.Decimal(5))
    
    def test_div_formula_2(self): 
        wb.set_cell_contents(name, 'a1', '50')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'd1', '=b1/a1')  # 0.2
        self.assertEqual(wb.get_cell_value(name, 'd1'), decimal.Decimal(10)/decimal.Decimal(50))
    
    def test_div_formula_3(self): 
        wb.set_cell_contents(name, 'e1', '=a1/b1/5')  # 1
        self.assertEqual(wb.get_cell_value(name, 'e1'), decimal.Decimal(1))

    # cell referencing
    def test_cell_reference_1(self):
        wb.set_cell_contents(name, 'a1', '=a2')
        self.assertEqual(wb.get_cell_value(name, 'a1'), decimal.Decimal())
        wb.set_cell_contents(name, 'a2', '5')
        self.assertEqual(wb.get_cell_value(name, 'a1'), decimal.Decimal(5))
    
    # errors
    # cycles
    def test_error_1(self): 
        wb.set_cell_contents(name, "A1", "=Nonexistent!a1")
        self.assertIsInstance(wb.get_cell_value(name, "a1"), sheets.CellError)
        self.assertIs(wb.get_cell_value(name, "a1").get_type(), sheets.CellErrorType.BAD_REFERENCE)
    
if __name__ == '__main__':
    unittest.main()
