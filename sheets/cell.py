import decimal
import lark
from lark.visitors import visit_children_decor

class FormulaEvaluater(lark.visitors.Interpreter):

    @visit_children_decor
    def add_expr(self, values):
        if values[1] == '+':
            return values[0] + values[2]
        elif values[1] == '-':
            return values[0] - values[2]
        else:
            assert False, 'Unexpected operator: ' + values[1]

    @visit_children_decor
    def mul_expr(self, values):
        if values[1] == '*':
            return values[0] * values[2]
        elif values[1] == '/':
            if values[2] == decimal.Decimal('0'):
                return '#DIV/0!'
            return values[0] / values[2]
        else:
            assert False, 'Unexpected operator: ' + values[1]
    
    def error(self, tree):
        return tree.children[0]

    def number(self, tree):
        return decimal.Decimal(tree.children[0])

    def string(self, tree):
        return tree.children[0][1: -1]

parser = lark.Lark.open('formulas.lark', start='formula')
f_evaluater = FormulaEvaluater()

def cell_eval(content):
    if content[0] == '=':
        return f_evaluater.visit(parser.parse(content))
    elif content[0] == '\'':
        return content[1:]
    elif content[0]:
        return

class Cell:
    
    content = None
    value = None
    dependencies = []

    def __init__(self, content):
        self.content = content
        self.value = cell_eval(self.content)
    
    def get(self):
        return self.value

    def set(self, new_content):
        self.content = new_content
