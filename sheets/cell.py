#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from .cellerrortype import *
from .cellerror import *
import decimal 
import lark
import logging
from lark.visitors import visit_children_decor

class _Cell():
    # constructor 
    def __init__(self, workbook, sheet_name: str, location: str):
        self.contents = None
        self.display_contents = None
        self.value_evaluator = None
        self.value = None
        self.workbook = workbook
        self.sheet_name = sheet_name
        self.location = location

    def __repr__(self):
        return self.contents

    # set contents as given string
    def set_contents(self, contents: str):
        self.contents = contents.upper()
        self.display_contents = contents
        # instiate the right CellValue class type depending on the case
        if self.contents[0] == '=':
            self.value_evaluator = CellValueFormula()
        elif self.contents[0] == '\'':
            self.value_evaluator = CellValueString()
        else:
            try:
                decimal.Decimal(self.contents)
                self.value_evaluator = CellValueNumber()
            except decimal.InvalidOperation:
                self.value_evaluator = CellValueString()
        try:
            self.value = self.value_evaluator.get_value(self)
        except AssertionError:
            detail = 'Bad reference to non-existent sheet'
            self.value = CellError(CellErrorType.BAD_REFERENCE, detail)
        except:
            detail = 'Cannot be parsed; please check input'
            self.value = CellError(CellErrorType.PARSE_ERROR, detail)

    # return literal contents of cell
    def get_contents(self):
        return self.display_contents

    # return literal contents of cell
    def get_display_contents(self):
        return self.display_contents

    # inform workbook of dependency between this cell and another cell
    def add_dependency(self, location: str, sheet_name: str = None):    
        if location == None:
            logging.info("Cell: add_dependency: could not add dependency - NoneType")
            return
        if sheet_name == None:
            sheet_name = self.sheet_name
        self.workbook.add_dependency(self, location, sheet_name)
    
    # return value calculated from cell contents
    def get_value(self):
        if self.contents is None:
            return None
        elif isinstance(self.value, CellError):
            return self.value
        self.value = self.value_evaluator.get_value(self)
        return self.value
    
class CellValueString():
    def get_value(self, cell: _Cell):
        try:
            if cell.display_contents[0] == '\'':
                return cell.display_contents[1:]
            err_type = CellErrorType(cell.contents)
            detail = f"Written error: {cell.display_contents}"
            return CellError(err_type, detail)
        except:
            return cell.display_contents

class CellValueNumber():
    def get_value(self, cell: _Cell):
        return decimal.Decimal(cell.contents)

class CellValueFormula():
    def get_value(self, cell: _Cell):
        parser = lark.Lark.open('formulas.lark', rel_to=__file__, start='formula')
        evaluator = FormulaEvaluator(cell.workbook, cell.sheet_name, cell)
        tree = parser.parse(cell.contents)
        value = evaluator.visit(tree)
        return value

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
    def __init__(self, workbook, sheet_name, parent_cell: _Cell):
       self.workbook = workbook
       self.sheet_name = sheet_name
       self.parent_cell = parent_cell

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
        return decimal.Decimal(tree.children[0])
    
    def string(self, tree):
        return tree.children[0].value[1:-1]
    
    def parens(self, tree):
        result = self.visit(tree.children[0])
        return result

    def sheetname(self, tree):
        return tree.children[0]

    def cell(self, tree):
        if (len(tree.children) == 1):
            self.parent_cell.add_dependency(tree.children[0])
            other_cell = self.workbook.get_dependent_cell_value(self.sheet_name, tree.children[0])
            if other_cell == None:
                return None
            else:
                return other_cell
        else:
            self.parent_cell.add_dependency(tree.children[1], tree.children[0])
            other_cell = self.workbook.get_dependent_cell_value(tree.children[0], tree.children[1])
            if other_cell == None:
                return None
            else:
                return other_cell 
