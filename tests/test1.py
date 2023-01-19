import decimal
from workbook import *
from cell_error import *

# Make a new empty workbook 
wb = Workbook()
(index, name) = wb.new_sheet()

class TestWorkbook():
    # create cells
    # numbers
    def test_num_cell_1(self): 
        wb.set_cell_contents(name, 'a1', '10')
        if (wb.get_cell_value(name, 'a1') == 10):
            print("test_num_cell_1 passed")
        else:
            print("test_num_cell_1 failed")
    
    def test_num_cell_2(self): 
        wb.set_cell_contents(name, 'b1', '1234567890')
        if (wb.get_cell_value(name, 'b1') == 1234567890):
            print("test_num_cell_2 passed")
        else:
            print("test_num_cell_2 failed")
        
    def test_num_cell_3(self): 
        wb.set_cell_contents(name, 'c1', '=-1234567890')
        if (wb.get_cell_value(name, 'c1') == -1234567890):
            print("test_num_cell_3 passed")
        else:
            print("test_num_cell_3 failed")
    
    def test_num_cell_4(self): 
        wb.set_cell_contents(name, 'a1', '   10')
        if (wb.get_cell_value(name, 'a1') == 10):
            print("test_num_cell_4 passed")
        else:
            print("test_num_cell_4 failed")

    # strings 
    def test_string_cell_1(self): 
        wb.set_cell_contents(name, 'a1', "one two three")
        if (wb.get_cell_value(name, 'a1') == "one two three"):
            print("test_string_cell_1 passed")
        else:
            print("test_string_cell_1 failed")
            print(wb.get_cell_value(name, 'a1'))

    def test_string_cell_2(self): 
        wb.set_cell_contents(name, 'b1', " ")
        if (wb.get_cell_value(name, 'b1') == " "):
            print("test_string_cell_2 passed")
        else:
            print("test_string_cell_2 failed")
            print(wb.get_cell_value(name, 'b1'))

    def test_string_cell_3(self): 
        wb.set_cell_contents(name, 'c1', '   one   ')
        if (wb.get_cell_value(name, 'c1') == '   one   '):
            print("test_string_cell_3 passed")
        else:
            print("test_string_cell_3 failed")

    # test functions
    # add_expr
    def test_add_formula_1(self): 
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'b1', '20')
        wb.set_cell_contents(name, 'c1', '=a1+b1')  # 30
        if (wb.get_cell_value(name, 'c1') == 30):
            print("test_add_formula_1 passed")
        else:
            print("test_add_formula_1 failed")
    
    def test_add_formula_2(self): 
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'b1', '20')
        wb.set_cell_contents(name, 'd1', '=a1-b1')  # -10
        if (wb.get_cell_value(name, 'd1') == -10):
            print("test_add_formula_2 passed")
        else:
            print("test_add_formula_2 failed")
    
    def test_add_formula_3(self): 
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'b1', '20')
        wb.set_cell_contents(name, 'e1', '=(a1+b1)')  # 30
        if (wb.get_cell_value(name, 'e1') == 30):
            print("test_add_formula_3 passed")
        else:
            print("test_add_formula_3 failed")
    
    def test_add_formula_4(self): 
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'b1', '20')
        wb.set_cell_contents(name, 'f1', '=(b1-a1+b1)+(-b1-a1-a1)+b1')  # 10
        if (wb.get_cell_value(name, 'f1') == 10):
            print("test_add_formula_4 passed")
        else:
            print("test_add_formula_4 failed")
        
    # concat_expr
    def test_concat_formula_1(self): 
        wb.set_cell_contents(name, 'a1', "one")
        wb.set_cell_contents(name, 'b1', "two")
        wb.set_cell_contents(name, 'c1', "=a1&b1") 
        if (wb.get_cell_value(name, 'c1') == "onetwo"):
            print("test_concat_formula_1 passed")
        else:
            print("test_concat_formula_1 failed")
            print(wb.get_cell_value(name, 'c1'))
    
    def test_concat_formula_2(self): 
        wb.set_cell_contents(name, 'a1', "one")
        wb.set_cell_contents(name, 'b1', "two")
        wb.set_cell_contents(name, 'd1', "=a1&\" \"&b1") 
        if (wb.get_cell_value(name, 'd1') == "one two"):
            print("test_concat_formula_2 passed")
        else:
            print("test_concat_formula_2 failed")
    
    def test_concat_formula_3(self): 
        wb.set_cell_contents(name, 'e1', "=7&9") 
        if (wb.get_cell_value(name, 'e1') == "79"):
            print("test_concat_formula_3 passed")
        else:
            print("test_concat_formula_3 failed")
            print(wb.get_cell_value(name, 'e1'))
    
    # mul_expr (multiply)
    def test_mul_formula_1(self): 
        wb.set_cell_contents(name, 'a1', '50')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'c1', '=a1*b1')  # 500
        if (wb.get_cell_value(name, 'c1') == 500):
            print("test_mul_formula_1 passed")
        else:
            print("test_mul_formula_1 failed")
    
    def test_mul_formula_2(self): 
        wb.set_cell_contents(name, 'a1', '50')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'd1', '=a1*b1*10000')  # 5000000
        if (wb.get_cell_value(name, 'd1') == 5000000):
            print("test_mul_formula_2 passed")
        else:
            print("test_mul_formula_2 failed")
    
    def test_mul_formula_3(self): 
        wb.set_cell_contents(name, 'a1', '50')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'e1', '=a1*b1*-1')  # -500
        if (wb.get_cell_value(name, 'e1') == -500):
            print("test_mul_formula_3 passed")
        else:
            print("test_mul_formula_3 failed")
    
    # mul_expr (divide)
    def test_div_formula_1(self): 
        wb.set_cell_contents(name, 'a1', '50')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'c1', '=a1/b1')  # 5
        if (wb.get_cell_value(name, 'c1') == decimal.Decimal(5)):
            print("test_div_formula_1 passed")
        else:
            print("test_div_formula_1 failed")
            print(wb.get_cell_value(name, 'c1'))
    
    def test_div_formula_2(self): 
        wb.set_cell_contents(name, 'd1', '=b1/a1')  # 0.2
        if (wb.get_cell_value(name, 'd1') > decimal.Decimal(0.1999) and wb.get_cell_value(name, 'd1') < decimal.Decimal(0.2001)):
            print("test_div_formula_2 passed")
        else:
            print("test_div_formula_2 failed")
            print(wb.get_cell_value(name, 'd1'))
    
    def test_div_formula_3(self): 
        wb.set_cell_contents(name, 'e1', '=a1/b1/5')  # 1
        if (wb.get_cell_value(name, 'e1') == 1):
            print("test_div_formula_3 passed")
        else:
            print("test_div_formula_3 failed")
    
    # errors
    # cycles
    def test_error_1(self): 
        # value should be a CellError with type BAD_REFERENCE
        value = wb.get_cell_value(name, 'd3')
        wb.set_cell_contents("Sheet1", "A1", "=Sheet1!a2&Sheet1!a3")
        wb.set_cell_contents("Sheet1", "A2", "=Sheet1!a1&Sheet1!a3")
        wb.set_cell_contents("Sheet1", "A3", "=Sheet1!a1&Sheet1!a2")
        if (type(wb.get_cell_contents()) == CellError and wb.get_cell_contents().error_type == "#CIRCREF!"):
            print("test_error_1 passed")
        else:
            print("test_error_1 failed")
    
   # case sensitivity
    def test_case_sensitivity_1(self):
        wb.set_cell_contents("SHEET1", "A1", "=f1")
        if wb.get_cell_value("sheet1", "a1") == decimal.Decimal():
            print("test_case_sensitivity_1 passed")
        else:
            print("test_case_sensitivity_1 failed")
    
    def test_case_sensitivity_2(self):
        wb.new_sheet("SHEET1") # should result in an error
        print(wb.list_sheets())
        #if wb.get_cell_value("sheet1", "a1") == decimal.Decimal():
        #    print("test_case_sensitivity_2 passed")
        #else:
        #    print("test_case_sensitivity_2 failed")

    def test_case_sensitivity_3(self):
        wb.set_cell_contents("SHEET1", "A1", "=f1")
        if wb.get_cell_value("sheet1", "a1") == decimal.Decimal():
            print("test_case_sensitivity_3 passed")
        else:
            print("test_case_sensitivity_3 failed")

    # scale test
    def test_scale_1(self):
        for i in range(1, 1001):
            wb.set_cell_contents(name, 'a' + str(i), str(i))
        wb.set_cell_contents(name, 'a1001', '=a1+a2')
        print('test_scale_1 (a) completed')
        for i in range(1, 1001):
            wb.set_cell_contents(name, 'b' + str(i), str(i))
        wb.set_cell_contents(name, 'b1001', '=b1+b2')
        print('test_scale_1 (b) completed')
        for i in range(1, 1001):
            wb.set_cell_contents(name, 'c' + str(i), str(i))
        wb.set_cell_contents(name, 'c1001', '=c1+c2')
        print('test_scale_1 (c) completed')
        if (wb.get_cell_value(name, 'a1001') == 3) and (wb.get_cell_value(name, 'b1001') == 3) and (wb.get_cell_value(name, 'c1001') == 3):
            print('test_scale_1 passed')
        else:
            print('test_scale_1 failed')
    
    def test_scale_2(self):    
        for i in range(1, 10000):
            wb.set_cell_contents(name, 'a' + str(i), str(i))
        wb.set_cell_contents(name, 'a1001' + str(i), '=a1+a2')
        for i in range(1, 10000):
            wb.set_cell_contents(name, 'b' + str(i), str(i))
            wb.set_cell_contents(name, 'b1001' + str(i), '=')
        for i in range(1, 10000):
            wb.set_cell_contents(name, 'c' + str(i), str(i))
        wb.set_cell_contents(name, 'c1001' + str(i), '=c1+c2')
    



    
tw = TestWorkbook()
tw.test_num_cell_2()
tw.test_num_cell_1()
tw.test_num_cell_3()
tw.test_num_cell_4()
tw.test_string_cell_1()
tw.test_string_cell_2()
tw.test_string_cell_3()

tw.test_add_formula_1()
tw.test_add_formula_2()
tw.test_add_formula_3()

#wb.graph.print()

tw.test_concat_formula_1()
tw.test_concat_formula_2()
tw.test_concat_formula_3()

tw.test_mul_formula_1()
tw.test_mul_formula_2()
tw.test_mul_formula_3()

tw.test_div_formula_1()
tw.test_div_formula_2()
tw.test_div_formula_3()

tw.test_case_sensitivity_1()
tw.test_case_sensitivity_2()
#tw.test_scale_1()
#tw.test_scale_2()




