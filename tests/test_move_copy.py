import context
import unittest
import decimal
import sheets

# Make a new empty workbook 
wb = sheets.Workbook()
(_, name) = wb.new_sheet()
(_, name2) = wb.new_sheet()

class TestWorkbook(unittest.TestCase):
    # create cells
    # numbers
    def test_copy_cells_1(self): 
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'b2', '10')
        wb.set_cell_contents(name, 'b3', '10')

        wb.copy_cells(name, 'a1', 'b3', 'c1')

        self.assertEqual(wb.get_cell_value(name, 'a1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'a2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'a3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'b1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b3'), 10)

        self.assertEqual(wb.get_cell_value(name, 'c1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'c2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'c3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'd1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'd2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'd3'), 10)

        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)
        wb.set_cell_contents(name, 'c3', None)
        wb.set_cell_contents(name, 'd1', None)
        wb.set_cell_contents(name, 'd2', None)
        wb.set_cell_contents(name, 'd3', None)
    
    def test_copy_cells_2(self):
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'b2', '10')
        wb.set_cell_contents(name, 'b3', '10')

        wb.copy_cells(name, 'a1', 'b3', 'b1')

        self.assertEqual(wb.get_cell_value(name, 'a1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'a2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'a3'), 20)

        self.assertEqual(wb.get_cell_value(name, 'b1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'c1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'c2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'c3'), 10)

        wb.set_cell_contents(name, 'b1', None)
        wb.set_cell_contents(name, 'b2', None)
        wb.set_cell_contents(name, 'b3', None)
        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)
        wb.set_cell_contents(name, 'c3', None)
    
    def test_copy_cells_3(self):
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '30')
        wb.set_cell_contents(name, 'b2', '40')
        wb.set_cell_contents(name, 'b3', '50')

        wb.copy_cells(name, 'b3', 'a1', 'b1')

        self.assertEqual(wb.get_cell_value(name, 'a1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'a2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'a3'), 20)

        self.assertEqual(wb.get_cell_value(name, 'b1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'c1'), 30)
        self.assertEqual(wb.get_cell_value(name, 'c2'), 40)
        self.assertEqual(wb.get_cell_value(name, 'c3'), 50)

        wb.set_cell_contents(name, 'b1', None)
        wb.set_cell_contents(name, 'b2', None)
        wb.set_cell_contents(name, 'b3', None)
        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)
        wb.set_cell_contents(name, 'c3', None)

    def test_copy_cells_4(self):
        wb.set_cell_contents(name, 'a1', '2.2')
        wb.set_cell_contents(name, 'a2', '4.5')
        wb.set_cell_contents(name, 'b1', '5.3')
        wb.set_cell_contents(name, 'b2', '3.1')
        wb.set_cell_contents(name, 'c1', '=A1*B1')
        wb.set_cell_contents(name, 'c2', '=A2*B2')

        wb.copy_cells(name, 'c1', 'c2', 'b1')

        self.assertEqual(wb.get_cell_value(name, 'a1'), decimal.Decimal('2.2'))
        self.assertEqual(wb.get_cell_value(name, 'a2'), decimal.Decimal('4.5'))

        self.assertEqual(wb.get_cell_contents(name, 'b1'), '= #REF! * A1')
        self.assertEqual(wb.get_cell_contents(name, 'b2'), '= #REF! * A2')

        wb.set_cell_contents(name, 'a1', None)
        wb.set_cell_contents(name, 'a2', None)
        wb.set_cell_contents(name, 'b1', None)
        wb.set_cell_contents(name, 'b2', None)
        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)
 
    def test_copy_cells_5(self):
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'b2', '10')
        wb.set_cell_contents(name, 'b3', '10')

        wb.copy_cells(name, 'a1', 'b3', 'a1', name2)

        self.assertEqual(wb.get_cell_value(name, 'a1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'a2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'a3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'b1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b3'), 10)
        
        self.assertEqual(wb.get_cell_value(name2, 'a1'), 10)
        self.assertEqual(wb.get_cell_value(name2, 'a2'), 10)
        self.assertEqual(wb.get_cell_value(name2, 'a3'), 20)
        self.assertEqual(wb.get_cell_value(name2, 'b1'), 10)
        self.assertEqual(wb.get_cell_value(name2, 'b2'), 10)
        self.assertEqual(wb.get_cell_value(name2, 'b3'), 10)

        wb.set_cell_contents(name2, 'a1', None)
        wb.set_cell_contents(name2, 'a2', None)
        wb.set_cell_contents(name2, 'a3', None)
        wb.set_cell_contents(name2, 'b1', None)
        wb.set_cell_contents(name2, 'b2', None)
        wb.set_cell_contents(name2, 'b3', None)
    
    def test_copy_cells_6(self):
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '30')
        wb.set_cell_contents(name, 'b2', '40')
        wb.set_cell_contents(name, 'b3', '50')

        wb.copy_cells(name, 'a3', 'b1', 'b1')

        self.assertEqual(wb.get_cell_value(name, 'a1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'a2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'a3'), 20)

        self.assertEqual(wb.get_cell_value(name, 'b1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'c1'), 30)
        self.assertEqual(wb.get_cell_value(name, 'c2'), 40)
        self.assertEqual(wb.get_cell_value(name, 'c3'), 50)

        wb.set_cell_contents(name, 'b1', None)
        wb.set_cell_contents(name, 'b2', None)
        wb.set_cell_contents(name, 'b3', None)
        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)
        wb.set_cell_contents(name, 'c3', None)

    def test_move_cells_1(self):  
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'b2', '10')
        wb.set_cell_contents(name, 'b3', '10')

        wb.move_cells(name, 'a1', 'b3', 'c1')

        self.assertEqual(wb.get_cell_value(name, 'a1'), None)
        self.assertEqual(wb.get_cell_value(name, 'a2'), None)
        self.assertEqual(wb.get_cell_value(name, 'a3'), None)
        self.assertEqual(wb.get_cell_value(name, 'b1'), None)
        self.assertEqual(wb.get_cell_value(name, 'b2'), None)
        self.assertEqual(wb.get_cell_value(name, 'b3'), None)

        self.assertEqual(wb.get_cell_value(name, 'c1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'c2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'c3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'd1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'd2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'd3'), 10)
        
        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)
        wb.set_cell_contents(name, 'c3', None)
        wb.set_cell_contents(name, 'd1', None)
        wb.set_cell_contents(name, 'd2', None)
        wb.set_cell_contents(name, 'c3', None)
    
    def test_move_cells_2(self):
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '10')
        wb.set_cell_contents(name, 'b2', '10')
        wb.set_cell_contents(name, 'b3', '10')

        wb.move_cells(name, 'a1', 'b3', 'b1')

        self.assertEqual(wb.get_cell_value(name, 'a1'), None)
        self.assertEqual(wb.get_cell_value(name, 'a2'), None)
        self.assertEqual(wb.get_cell_value(name, 'a3'), None)

        self.assertEqual(wb.get_cell_value(name, 'b1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'c1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'c2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'c3'), 10)

        wb.set_cell_contents(name, 'b1', None)
        wb.set_cell_contents(name, 'b2', None)
        wb.set_cell_contents(name, 'b3', None)
        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)
        wb.set_cell_contents(name, 'c3', None)
    
    def test_move_cells_3(self):
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '30')
        wb.set_cell_contents(name, 'b2', '40')
        wb.set_cell_contents(name, 'b3', '50')

        wb.move_cells(name, 'b3', 'a1', 'b1')

        self.assertEqual(wb.get_cell_value(name, 'a1'), None)
        self.assertEqual(wb.get_cell_value(name, 'a2'), None)
        self.assertEqual(wb.get_cell_value(name, 'a3'), None)

        self.assertEqual(wb.get_cell_value(name, 'b1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'c1'), 30)
        self.assertEqual(wb.get_cell_value(name, 'c2'), 40)
        self.assertEqual(wb.get_cell_value(name, 'c3'), 50)

        wb.set_cell_contents(name, 'b1', None)
        wb.set_cell_contents(name, 'b2', None)
        wb.set_cell_contents(name, 'b3', None)
        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)
        wb.set_cell_contents(name, 'c3', None)

    def test_move_cells_4(self):
        wb.set_cell_contents(name, 'a1', '2.2')
        wb.set_cell_contents(name, 'a2', '4.5')
        wb.set_cell_contents(name, 'b1', '5.3')
        wb.set_cell_contents(name, 'b2', '3.1')
        wb.set_cell_contents(name, 'c1', '=A1*B1')
        wb.set_cell_contents(name, 'c2', '=A2*B2')

        wb.move_cells(name, 'c1', 'c2', 'b1')

        self.assertEqual(wb.get_cell_contents(name, 'b1'), '= #REF! * A1')
        self.assertEqual(wb.get_cell_contents(name, 'b2'), '= #REF! * A2')

        self.assertEqual(wb.get_cell_value(name, 'c1'), None)
        self.assertEqual(wb.get_cell_value(name, 'c2'), None)

        wb.set_cell_contents(name, 'a1', None)
        wb.set_cell_contents(name, 'a2', None)
        wb.set_cell_contents(name, 'b1', None)
        wb.set_cell_contents(name, 'b2', None)
        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)

    def test_move_cells_5(self): 
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '30')
        wb.set_cell_contents(name, 'b2', '40')
        wb.set_cell_contents(name, 'b3', '50')

        wb.move_cells(name, 'a1', 'b3', 'c1')

        self.assertEqual(wb.get_cell_value(name, 'a1'), None)
        self.assertEqual(wb.get_cell_value(name, 'a2'), None)
        self.assertEqual(wb.get_cell_value(name, 'a3'), None)
        self.assertEqual(wb.get_cell_value(name, 'b1'), None)
        self.assertEqual(wb.get_cell_value(name, 'b2'), None)
        self.assertEqual(wb.get_cell_value(name, 'b3'), None)

        self.assertEqual(wb.get_cell_value(name, 'c1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'c2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'c3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'd1'), 30)
        self.assertEqual(wb.get_cell_value(name, 'd2'), 40)
        self.assertEqual(wb.get_cell_value(name, 'd3'), 50)

        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)
        wb.set_cell_contents(name, 'c3', None)
        wb.set_cell_contents(name, 'd1', None)
        wb.set_cell_contents(name, 'd2', None)
        wb.set_cell_contents(name, 'c3', None)
    
    def test_move_cells_6(self):
        wb.set_cell_contents(name, 'a1', '=$a2')
        wb.set_cell_contents(name, 'a2', 'a2')
        wb.set_cell_contents(name, 'a4', 'a4')
        wb.set_cell_contents(name, 'b1', 'b1')
        wb.set_cell_contents(name, 'b2', 'b2')
        wb.set_cell_contents(name, 'c1', 'c1')
        wb.set_cell_contents(name, 'c4', 'c4')

        wb.move_cells(name, 'a1', 'a1', 'c3')

        self.assertEqual(wb.get_cell_value(name, 'a1'), None)
        self.assertEqual(wb.get_cell_value(name, 'c3'), 'a4')
        self.assertEqual(wb.get_cell_contents(name, 'c3'), '= $A4')

        wb.set_cell_contents(name, 'a1', None)

    def test_move_cells_7(self):
        wb.set_cell_contents(name, 'a1', '=a$2')
        wb.set_cell_contents(name, 'a2', 'a2')
        wb.set_cell_contents(name, 'c2', 'c2')
        wb.set_cell_contents(name, 'c4', 'c4')

        wb.move_cells(name, 'a1', 'a1', 'c3')

        self.assertEqual(wb.get_cell_value(name, 'c3'), 'c2')
        self.assertEqual(wb.get_cell_contents(name, 'c3'), '= C$2')
        self.assertEqual(wb.get_cell_value(name, 'a1'), None)

        wb.set_cell_contents(name, 'a1', None)
    
    def test_move_cells_8(self):
        wb.set_cell_contents(name, 'a1', '=$a$2')
        wb.set_cell_contents(name, 'a2', 'a2')
        wb.set_cell_contents(name, 'a4', 'a4')
        wb.set_cell_contents(name, 'b1', 'b1')
        wb.set_cell_contents(name, 'b2', 'b2')
        wb.set_cell_contents(name, 'c2', 'c2')
        wb.set_cell_contents(name, 'c4', 'c4')

        wb.move_cells(name, 'a1', 'a1', 'c3')

        self.assertEqual(wb.get_cell_value(name, 'c3'), 'a2')
        self.assertEqual(wb.get_cell_contents(name, 'c3'), '= $A$2')
        self.assertEqual(wb.get_cell_value(name, 'a1'), None)

        wb.set_cell_contents(name, 'a1', None)
        wb.set_cell_contents(name, 'a2', None)
        wb.set_cell_contents(name, 'a4', None)
        wb.set_cell_contents(name, 'b1', None)
        wb.set_cell_contents(name, 'b2', None)
        wb.set_cell_contents(name, 'c2', None)
        wb.set_cell_contents(name, 'c3', None)
        wb.set_cell_contents(name, 'c4', None)

    def test_move_cells_9(self):
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '20')
        wb.set_cell_contents(name, 'b2', '30')
        wb.set_cell_contents(name, 'b3', '40')

        wb.move_cells(name, 'b3', 'a1', 'a1', name2)

        self.assertEqual(wb.get_cell_value(name, 'a1'), None)
        self.assertEqual(wb.get_cell_value(name, 'a2'), None)
        self.assertEqual(wb.get_cell_value(name, 'a3'), None)
        self.assertEqual(wb.get_cell_value(name, 'b1'), None)
        self.assertEqual(wb.get_cell_value(name, 'b2'), None)
        self.assertEqual(wb.get_cell_value(name, 'b3'), None)

        self.assertEqual(wb.get_cell_value(name2, 'a1'), 10)
        self.assertEqual(wb.get_cell_value(name2, 'a2'), 10)
        self.assertEqual(wb.get_cell_value(name2, 'a3'), 20)
        self.assertEqual(wb.get_cell_value(name2, 'b1'), 20)
        self.assertEqual(wb.get_cell_value(name2, 'b2'), 30)
        self.assertEqual(wb.get_cell_value(name2, 'b3'), 40)

        wb.set_cell_contents(name2, 'a1', None)
        wb.set_cell_contents(name2, 'a2', None)
        wb.set_cell_contents(name2, 'a3', None)
        wb.set_cell_contents(name2, 'b1', None)
        wb.set_cell_contents(name2, 'b2', None)
        wb.set_cell_contents(name2, 'b3', None)

    def test_move_cells_10(self):
        wb.set_cell_contents(name, 'a1', '10')
        wb.set_cell_contents(name, 'a2', '=a1')
        wb.set_cell_contents(name, 'a3', '=a1+a2')
        wb.set_cell_contents(name, 'b1', '30')
        wb.set_cell_contents(name, 'b2', '40')
        wb.set_cell_contents(name, 'b3', '50')

        wb.move_cells(name, 'a3', 'b1', 'b1')

        self.assertEqual(wb.get_cell_value(name, 'a1'), None)
        self.assertEqual(wb.get_cell_value(name, 'a2'), None)
        self.assertEqual(wb.get_cell_value(name, 'a3'), None)

        self.assertEqual(wb.get_cell_value(name, 'b1'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b2'), 10)
        self.assertEqual(wb.get_cell_value(name, 'b3'), 20)
        self.assertEqual(wb.get_cell_value(name, 'c1'), 30)
        self.assertEqual(wb.get_cell_value(name, 'c2'), 40)
        self.assertEqual(wb.get_cell_value(name, 'c3'), 50)

        wb.set_cell_contents(name, 'b1', None)
        wb.set_cell_contents(name, 'b2', None)
        wb.set_cell_contents(name, 'b3', None)
        wb.set_cell_contents(name, 'c1', None)
        wb.set_cell_contents(name, 'c2', None)
        wb.set_cell_contents(name, 'c3', None)

if __name__ == '__main__':
    unittest.main()
