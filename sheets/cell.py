#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from cell_graph import *
import decimal 
import lark
import logging

class Cell():
    # constructor 
    def __init__(self, workbook, sheet_name: str, location: str, graph):
        self.contents = None
        self.display_contents = None
        self.value_evaluator = None
        self.value = None
        self.graph = graph
        self.workbook = workbook
        self.sheet_name = sheet_name
        self.location = location
        self.dependencies = []

    def __repr__(self):
        return self.contents

    # set contents as given string
    def set_contents(self, contents: str):
        self.contents = contents.upper()
        self.display_contents = contents
        # instiate the right CellValue class type depending on the case
        if self.contents[0] == '=':
            self.value_evaluator = CellValueFormula()
            parser = lark.Lark.open('formulas.lark', start='formula')
            evaluator = DependencyFinder(self)
            tree = parser.parse(self.contents)
            evaluator.cell(tree)
        else:
            parser = lark.Lark.open('formulas.lark', start='base')
            tree = parser.parse(contents)
            if (tree.data == 'number'):
                self.value_evaluator = CellValueNumber()
            else:
                self.value_evaluator = CellValueString()
        # check for dependencies

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
        dependent_cell = self.workbook.add_dependency(self, location, sheet_name)
        self.dependencies.append(dependent_cell)
    
    # return value calculated from cell contents
    def get_value(self):
        if self.value == None:
            self.value = self.value_evaluator.get_value(self)
        return self.value
    
class CellValueString():
    def get_value(self, cell: Cell ):
        parser = lark.Lark.open('formulas.lark', start='base')
        tree = parser.parse(cell.display_contents)
        return tree.children[0].value[1:-1]

class CellValueNumber():
    def get_value(self, cell: Cell):
        parser = lark.Lark.open('formulas.lark', start='base')
        tree = parser.parse(cell.display_contents)
        return decimal.Decimal(tree.children[0])

class CellValueFormula():
    def get_value(self, cell: Cell):
        parser = lark.Lark.open('formulas.lark', start='formula')
        evaluator = FormulaEvaluator(cell.workbook, cell.sheet_name)
        tree = parser.parse(cell.contents)
        value = evaluator.visit(tree)
        return value

class FormulaEvaluator(lark.visitors.Interpreter):
    def __init__(self, workbook, sheet_name):
       self.workbook = workbook
       self.sheet_name = sheet_name

    def add_expr(self, tree):
        values = self.visit_children(tree)
        if values[1] == '+':
            return values[0] + values[2]
        elif values[1] == '-':
            return values[0] - values[2]
        else:
            assert False, 'Unexpected operator: ' + values[1]

    def mul_expr(self, tree):
        values = self.visit_children(tree)
        if values[1] == '*':
            return values[0] * values[2]
        elif values[1] == '/':
            if values[2] == decimal.Decimal('0'):
                return '#DIV/0!'
            return values[0] / values[2]
        else:
            assert False, 'Unexpected operator: ' + values[1]

    def concat_expr(self, tree):
        values = self.visit_children(tree)
        return values[0] + values[1]

    def unary_op(self, tree):
        values = self.visit_children(tree)
        if values[0] == '+':
            return values[1]
        elif values[0] == '-':
            return -1 * values[1]
        else:
            assert False, 'Unexpected operator: ' + values[0]

    def error(self, tree):
        return tree.children[0]

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
            return self.workbook.get_dependent_cell_value(self.sheet_name, tree.children[0])
        else:
            return self.workbook.get_dependent_cell_value(tree.children[0], tree.children[1])

class DependencyFinder(lark.visitors.Interpreter):
    def __init__(self, parent_cell):
        self.parent_cell = parent_cell

    def cell(self, tree):
        values = self.visit_children(tree)
        if type(values) == None:
            logging.info("DependencyFinder: cell: NoneType value detected")
            return
        #print('parent: ' + self.parent_cell.location + ' values: ' + str(values))
        #print(values[0])
        if (values != None and tree.data == 'cell'):
            self.parent_cell.add_dependency(values[0])
