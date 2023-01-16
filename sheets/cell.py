import decimal
import lark
from cellerror import CellError
from cellerrortype import CellErrorType
from lark.visitors import visit_children_decor

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

class FormulaEvaluater(lark.visitors.Interpreter):

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
    
    @visit_children_decor
    def concat_expr(self, values):
        return values[0] + values[1]

    def error(self, tree):
        return CellError(CellErrorType(tree.children[0]), tree.children[0])

    def number(self, tree):
        return decimal.Decimal(tree.children[0])

    def string(self, tree):
        return tree.children[0][1: -1]
    
    def parens(self, tree):
        return self.visit(tree.children[0])

    def cell(self, tree):
        return tree.children[0]

def cell_eval(content):
    parser = lark.Lark.open('formulas.lark', start='formula')
    f_evaluater = FormulaEvaluater()
    
    if content[0] == '=':
        try:
            return f_evaluater.visit(parser.parse(content))
        except Exception as err:
            detail = f'The formula could not be parsed: {content}'
            return CellError(CellErrorType.PARSE_ERROR, detail, err)
    elif content[0] == '\'':
        return content[1:]
    else:
        try:
            return decimal.Decimal(content)
        except decimal.InvalidOperation:
            return content

class Cell:
    
    def __init__(self, content: str):
        self._content = content
        self._value = cell_eval(self._content)
        self._dependencies = []
    
    def get_value(self):
        return self._value

    def set_content(self, new_content):
        self._content = new_content
        self._value = cell_eval(self._content)

    def update_value(self):
        self._value = cell_eval(self._content)

    def get_dependencies(self):
        return self._dependencies
