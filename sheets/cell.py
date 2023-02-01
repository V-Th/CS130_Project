#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .cellerrortype import *
from .cellerror import *
import decimal 
import lark
from lark.visitors import visit_children_decor
import json
from json import JSONEncoder

# Parser for cell contents
parser = lark.Lark.open('formulas.lark', rel_to=__file__, start='formula')

class _Cell():
    # constructor 
    def __init__(self, workbook, sheet_name: str, location: str):
        self.contents = None
        self.value = None
        self.workbook = workbook
        self.sheet_name = sheet_name
        self.location = location

    def __repr__(self):
        return self.contents

    def toJSON(self):
        return json.dumps(self.contents)

    def _is_error(self):
        try:
            err_type = CellErrorType(self.contents)
            detail = f"Written error: {self.contents}"
            self.value = CellError(err_type, detail)
            return True
        except:
            return False

    def _is_number_or_string(self):
        try:
            self.value = decimal.Decimal(self.contents)
        except:
            self.value = self.contents

    def _eval_formula(self):
        evaluator = FormulaEvaluator(self.workbook, self.sheet_name, self)
        try:
            tree = parser.parse(self.contents)
            self.value =  evaluator.visit(tree)
            if self.value is None:
                self.value = decimal.Decimal()
        except AssertionError:
            detail = 'Bad reference to non-existent sheet'
            self.value = CellError(CellErrorType.BAD_REFERENCE, detail)
        except:
            detail = 'Cannot be parsed; please check input'
            self.value = CellError(CellErrorType.PARSE_ERROR, detail)
        return

    def update_value(self):
        if self.contents is None:
            self.value = None
        elif self.contents[0] == '=':
            self._eval_formula()
        elif self.contents[0] == '\'':
            self.value = self.contents[1:]
        else:
            if not self._is_error():
                self._is_number_or_string()

    # set contents as given string and update its value
    def set_contents(self, contents: str):
        if contents is None:
            self.contents = None
        elif not contents.strip():
            self.contents = None
        else:
            self.contents = contents.strip()

    # return literal contents of cell
    def get_contents(self):
        return self.contents
    
    # return value calculated from cell contents
    def get_value(self):
        return self.value

def check_arithmetic_input(value):
    if isinstance(value, (decimal.Decimal, CellError)):
        return value
    elif value is None:
        return decimal.Decimal()
    try:
        return decimal.Decimal(value)
    except decimal.InvalidOperation as err:
        detail = f'The value cannot be parsed into a number: {value}'
        return CellError(CellErrorType.TYPE_ERROR, detail, err)

def check_inputs(value1, value2):
    check_v1 = check_arithmetic_input(value1)
    check_v2 = check_arithmetic_input(value2)
    if isinstance(check_v1, CellError):
        return check_v1
    elif isinstance(check_v2, CellError):
        return check_v2
    else:
        return check_v1, check_v2

def convert_str(value):
    if value is None:
        return ''
    elif isinstance(value, CellError):
        return value
    else:
        return str(value)

class FormulaEvaluator(lark.visitors.Interpreter):
    def __init__(self, workbook, sheet_name, this_cell: _Cell):
       self.wb = workbook
       self.sheet = sheet_name
       self.this_cell = this_cell

    @visit_children_decor
    def add_expr(self, values):
        check = check_inputs(values[0], values[2])
        if isinstance(check, CellError):
            return check
        v1, v2 = check
        if values[1] == '+':
            return v1 + v2
        elif values[1] == '-':
            return v1 - v2
        else:
            assert False, 'Unexpected operator: ' + values[1]

    @visit_children_decor
    def mul_expr(self, values):
        check = check_inputs(values[0], values[2])
        if isinstance(check, CellError):
            return check
        v1, v2 = check
        if values[1] == '*':
            return v1 * v2
        elif values[1] == '/':
            try:
                return v1 / v2
            except Exception as err:
                detail = "Cannot divide by 0"
                return CellError(CellErrorType.DIVIDE_BY_ZERO, detail, err)
        else:
            assert False, 'Unexpected operator: ' + values[1]

    @visit_children_decor
    def concat_expr(self, values):
        try:
            v1 = convert_str(values[0])
            v2 = convert_str(values[1])
            if isinstance(v1, CellError):
                return v1
            elif isinstance(v2, CellError):
                return v2
            else:
                return v1 + v2
        except:
            return CellError(CellErrorType.PARSE_ERROR, "Cannot parse inputs as strings for concatenation")

    @visit_children_decor
    def unary_op(self, values):
        v1 = check_arithmetic_input(values[1])
        if isinstance(v1, CellError):
            return v1
        if values[0] == '+':
            return v1
        elif values[0] == '-':
            return -v1
        else:
            assert False, 'Unexpected operator: ' + values[0]

    def error(self, tree):
        return CellError(CellErrorType(tree.children[0]), tree.children[0])

    def number(self, tree):
        num = tree.children[0]
        if '.' in num:
            num = num.rstrip('0').rstrip('.')
        return decimal.Decimal(num)
    
    def string(self, tree):
        return tree.children[0].value[1:-1]
    
    def parens(self, tree):
        return self.visit(tree.children[0])

    def cell(self, tree):
        if (len(tree.children) == 1):
            self.wb.add_dependency(self.this_cell, tree.children[0], self.sheet)
            other_cell = self.wb.get_cell_value(self.sheet, tree.children[0])
        else:
            sheet_name = tree.children[0]
            if sheet_name[0] == '\'':
                sheet_name = sheet_name[1:-1]
            self.wb.add_dependency(self.this_cell, tree.children[1], sheet_name)
            other_cell = self.wb.get_cell_value(sheet_name, tree.children[1])
        return other_cell
