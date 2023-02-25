# pylint: skip-file
import context
import decimal
import unittest
from sheets import *
from sheets import version

class TestMethods(unittest.TestCase):
    def setUp(self):
        self.workbook = Workbook()
        _, self.s1 = self.workbook.new_sheet()

    def test_bad_func(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '= BAD()')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.BAD_NAME)
        self.workbook.set_cell_contents(self.s1, 'a1', '= still_bad()')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.BAD_NAME)

    def test_AND(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '= AND(true, false)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= AND(true, true)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= AND(true, true, false)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= AND()')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))
        self.workbook.set_cell_contents(self.s1, 'a1', '= AND(0, 1, 0)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= AND(\"false\", \"false\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= AND(\"Nearl\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))

    def test_OR(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '= OR(true, false)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= OR(False, False)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= OR(False, true, false)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= OR()')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))
        self.workbook.set_cell_contents(self.s1, 'a1', '= OR(0, 1, 0)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= OR(\"false\", \"false\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= OR(\"Astesia\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))

    def test_NOT(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '= NOT(true)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= NOT(false)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= NOT(1)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= NOT()')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))
        self.workbook.set_cell_contents(self.s1, 'a1', '= NOT(true, false)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))
        self.workbook.set_cell_contents(self.s1, 'a1', '= NOT(\"Shining\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))
        self.workbook.set_cell_contents(self.s1, 'a1', '= NOT(\"false\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)

    def test_XOR(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '= XOR(true, false)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= XOR(true, true)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= XOR(true, true, false)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= XOR()')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))
        self.workbook.set_cell_contents(self.s1, 'a1', '= XOR(\"Kalsit\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))
        self.workbook.set_cell_contents(self.s1, 'a1', '= XOR(0, 1, \"false\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)

    def test_nested_boolean_logic(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '= OR(NOT(false), false)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= XOR(true, AND(true, true))')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= AND(true, OR(0, 1), NOT(0))')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= OR(XOR(), AND(1, 1))')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))
        self.workbook.set_cell_contents(self.s1, 'a1', '= NOT(XOR(\"Rosmontis\"))')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))

    def test_exact(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '= EXACT(\" \", \" \")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= EXACT(\"Bob\", \"bob\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= EXACT(\"hello\", \"hello\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= EXACT(\"hello world\", \"hello\"&\" world\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= EXACT(\" \")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))
        self.workbook.set_cell_contents(self.s1, 'a1', '= EXACT(\" \", \"hi\", \"bye\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType(5))
        self.workbook.set_cell_contents(self.s1, 'a1', '= EXACT(\"42\", 42)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a1', '= EXACT(\"TRUE\", TRUE)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)

    def test_isblank(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '= ISBLANK(a2)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a2', '1')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= ISBLANK(\"\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= ISBLANK(0)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a1', '= ISBLANK(FALSE)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)

    def test_iserror(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '= ISERROR(a2)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, False)
        self.workbook.set_cell_contents(self.s1, 'a2', '#ERROR!')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a2', '= bad formula')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, bool)
        self.assertEqual(a1_val, True)
        self.workbook.set_cell_contents(self.s1, 'a2', '= a2')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        a2_val = self.workbook.get_cell_value(self.s1, 'a2')
        self.assertIsInstance(a1_val, bool)
        self.assertIsInstance(a2_val, CellError)
        self.assertEqual(a1_val, True)
        self.assertEqual(a2_val.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.workbook.set_cell_contents(self.s1, 'a2', '= ISBLANK(a1)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        a2_val = self.workbook.get_cell_value(self.s1, 'a2')
        self.assertIsInstance(a1_val, CellError)
        self.assertIsInstance(a2_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.CIRCULAR_REFERENCE)
        self.assertEqual(a2_val.get_type(), CellErrorType.CIRCULAR_REFERENCE)

    def test_version(self):
        self.workbook.set_cell_contents(self.s1, 'a1', '= VERSION()')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, str)
        self.assertEqual(a1_val, str(version))

    def test_indirect(self):
        self.workbook.set_cell_contents(self.s1, 'a2', 'Phantasy')
        self.workbook.set_cell_contents(self.s1, 'a1', '= INDIRECT(\"a2\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, str)
        self.assertEqual(a1_val, "Phantasy")
        self.workbook.set_cell_contents(self.s1, 'a2', 'Star')
        self.workbook.set_cell_contents(self.s1, 'a1', '= INDIRECT(\"sheet1!a2\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, str)
        self.assertEqual(a1_val, "Star")
        self.workbook.set_cell_contents(self.s1, 'a2', 'Online')
        self.workbook.set_cell_contents(self.s1, 'a1', '= INDIRECT(\"Sheet1!\"&\"a2\")')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, str)
        self.assertEqual(a1_val, "Online")
        self.workbook.set_cell_contents(self.s1, 'a2', '2')
        self.workbook.set_cell_contents(self.s1, 'a1', '= INDIRECT(a2)')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, decimal.Decimal)
        self.assertEqual(a1_val, decimal.Decimal(2))
        self.workbook.set_cell_contents(self.s1, 'a2', '= a1')
        a1_val = self.workbook.get_cell_value(self.s1, 'a1')
        self.assertIsInstance(a1_val, CellError)
        self.assertEqual(a1_val.get_type(), CellErrorType.CIRCULAR_REFERENCE)

if __name__ == '__main__':
    unittest.main()
