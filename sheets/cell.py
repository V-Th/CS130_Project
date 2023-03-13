'''
The cell module implements the Cell class that store cell value and contents
and funcionality to parse formulas
'''
import json
import decimal
import lark
from lark.visitors import visit_children_decor
from .custom_func import DICTIONARY_FUNCTIONS
from .cellerror import CellError
from .cellerrortype import CellErrorType, str_to_error

# Characters for sheetname that require quotes
_REQUIRE_QUOTES = set(" .?!,:;!@#$%^&*()-")

# Comparsion of two differing types
_TYPE_VALUE = {
    bool: 2,
    str: 1,
    decimal.Decimal: 0
}

# Comparison-Empty Cell conversion
_COMPARISON_EMPTY_CELL = {
    str: "",
    decimal.Decimal: decimal.Decimal(),
    bool: False
}

# Comparison lambda operations
_COMPARISON_LAMBDAS = {
    "=": lambda a, b: a == b,
    "==": lambda a, b: a == b,
    "<>": lambda a, b: a != b,
    "!=": lambda a, b: a != b,
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
}

# Parser for cell contents
parser = lark.Lark.open('formulas.lark', rel_to=__file__, start='formula')

class _Cell():
    # constructor
    def __init__(self, workbook, sheet_name: str, location: str):
        self.contents = None
        self.tree = None
        self.value = None
        self.workbook = workbook
        self.location = location
        self.sheet_name = sheet_name

    def __repr__(self):
        return self.contents

    # pylint: disable=C0103
    def toJSON(self):
        '''
        returns JSON serialized representation of cell contents
        '''
        return json.dumps(self.contents)

    def _is_error(self):
        err_type = str_to_error(self.contents.upper())
        if err_type is None:
            return False
        detail = f"Written error: {self.contents.upper()}"
        self.value = CellError(err_type, detail)
        return True

    def _is_boolean(self):
        contents_upper = self.contents.upper()
        if contents_upper == 'TRUE':
            self.value = True
            return True
        if contents_upper == 'FALSE':
            self.value = False
            return True
        return False

    def _is_number_or_string(self):
        try:
            self.value = decimal.Decimal(self.contents)
        except decimal.DecimalException:
            self.value = self.contents

    def _eval_formula(self):
        if self.tree is None:
            detail = 'Cannot be parsed; please check input'
            self.value = CellError(CellErrorType.PARSE_ERROR, detail)
            return
        evaluator = FormulaEvaluator(self.workbook, self.sheet_name, self)
        try:
            self.value = evaluator.visit(self.tree)
            if self.value is None:
                self.value = decimal.Decimal()
        except AssertionError:
            detail = 'Bad reference to non-existent sheet'
            self.value = CellError(CellErrorType.BAD_REFERENCE, detail)

    def update_value(self):
        '''
        change value of existing cell
        '''
        if self.contents is None:
            self.value = None
        elif self.contents[0] == '=':
            self._eval_formula()
        elif self.contents[0] == '\'':
            self.value = self.contents[1:]
        else:
            if self._is_error():
                return
            if self._is_boolean():
                return
            self._is_number_or_string()

    def update_dependencies(self):
        '''
        Adds dependencies to the graph
        '''
        add_dep = self.workbook.add_dependency
        add_to_graph = AddDependencies(add_dep, self.sheet_name, self)
        add_to_graph.visit(self.tree)

    def set_contents(self, contents: str):
        '''
        set contents as given string and update its value
        if string represents formula, parse for value
        '''
        if contents is None:
            self.contents = None
            return
        if not contents.strip():
            self.contents = None
            return
        self.contents = contents.strip()
        if self.contents[0] == '=':
            try:
                self.tree = parser.parse(self.contents)
                self.update_dependencies()
            except lark.exceptions.LarkError:
                self.tree = None
                detail = 'Cannot be parsed; please check input'
                self.value = CellError(CellErrorType.PARSE_ERROR, detail)

    def get_contents(self):
        '''
        return literal contents of cell
        '''
        return self.contents

    def get_value(self):
        '''
        return value calculated from cell contents
        '''
        return self.value

    def rename_sheet(self, new_name, old_name):
        '''
        rename sheet referenced by cell contents
        '''
        if old_name.upper() not in self.contents.upper():
            return
        args = [old_name, new_name]
        evaluator = ContentManipulation(sheetname_manipulator, args)
        self.contents = '= '+ evaluator.transform(self.tree)
        self.tree = parser.parse(self.contents)

    # given another location, compare to this cell's location
    # return contents with cell references adjusted accordingly
    def get_relative_contents(self, x_diff, y_diff, new_sheet_name = None) -> str:
        '''
        given another location, compare to this cell's location
        return contents with cell references adjusted accordingly
        '''
        if self.contents[0] != '=':
            return self.contents
        if self.tree is None:
            return self.contents
        args = [self.workbook, x_diff, y_diff, new_sheet_name]
        evaluator = ContentManipulation(cellref_manipulator, args)
        return '= ' + evaluator.transform(self.tree)

def check_arithmetic_input(value):
    '''
    check if arithmetic formula can be parsed to a Decimal
    '''
    if isinstance(value, (decimal.Decimal, CellError)):
        return value
    if value is None:
        return decimal.Decimal()
    try:
        return decimal.Decimal(value)
    except decimal.InvalidOperation as err:
        detail = f'The value cannot be parsed into a number: {value}'
        return CellError(CellErrorType.TYPE_ERROR, detail, err)

def check_inputs(value1, value2):
    '''
    check validity of arithmetic inputs
    '''
    check_v1 = check_arithmetic_input(value1)
    check_v2 = check_arithmetic_input(value2)
    if isinstance(check_v1, CellError):
        return check_v1
    if isinstance(check_v2, CellError):
        return check_v2
    return check_v1, check_v2

def convert_str(value):
    '''
    return string representation of specified value
    '''
    if value is None:
        return ''
    if isinstance(value, CellError):
        return value
    if isinstance(value, bool):
        return str(value).upper()
    return str(value)

def compare_op(value1, value2, operator):
    '''
    operator should be a lambda expression
    Performs comparison: value1 > value2
    '''
    if isinstance(value1, CellError):
        return value1
    if isinstance(value2, CellError):
        return value2
    if isinstance(value1, type(value2)):
        if isinstance(value1, str):
            return operator(value1.lower(), value2.lower())
        return operator(value1, value2)
    type_val1 = _TYPE_VALUE[type(value1)]
    type_val2 = _TYPE_VALUE[type(value2)]
    return operator(type_val1, type_val2)

class AddDependencies(lark.visitors.Interpreter):
    '''
    Add the dependencies of the cell to the cellgraph
    '''
    def __init__(self, add_dep, sheet_name, this_cell: _Cell):
        self.add_dep = add_dep
        self.sheet = sheet_name
        self.this_cell = this_cell

    def function(self, tree):
        '''
        Ignore adding dependencies for certain functions
        '''
        custom_function = DICTIONARY_FUNCTIONS.get(tree.children[0])
        if custom_function is None:
            return
        _, dynamic_dep = custom_function
        if dynamic_dep:
            self.visit(tree.children[1])
            return
        for child in tree.children[1:]:
            if child is None:
                break
            self.visit(child)

    def cell(self, tree):
        '''
        Adds the cell references to the dependencies
        '''
        if len(tree.children) == 1:
            cellref = tree.children[0].replace('$', '')
            self.add_dep(self.this_cell, cellref, self.sheet)
        else:
            sheet_name = tree.children[0]
            if sheet_name[0] == '\'':
                sheet_name = sheet_name[1:-1]
            cellref = tree.children[1].replace('$', '')
            self.add_dep(self.this_cell, cellref, sheet_name)

class FormulaEvaluator(lark.visitors.Interpreter):
    '''
    parse value of cell formulas
    '''
    def __init__(self, workbook, sheet_name, this_cell):
        self.workbook = workbook
        self.sheet = sheet_name
        self.this_cell = this_cell

    @visit_children_decor
    def add_expr(self, values):
        '''
        evaluate an addition expressions
        '''
        check = check_inputs(values[0], values[2])
        if isinstance(check, CellError):
            return check
        v_1, v_2 = check
        if values[1] == '+':
            return v_1 + v_2
        if values[1] == '-':
            return v_1 - v_2
        assert False, 'Unexpected operator: ' + values[1]

    @visit_children_decor
    def mul_expr(self, values):
        '''
        evaluate a multiplication expression
        '''
        check = check_inputs(values[0], values[2])
        if isinstance(check, CellError):
            return check
        v_1, v_2 = check
        if values[1] == '*':
            return v_1 * v_2
        if values[1] == '/':
            try:
                return v_1 / v_2
            except ZeroDivisionError as err:
                detail = "Cannot divide by 0"
                return CellError(CellErrorType.DIVIDE_BY_ZERO, detail, err)
        assert False, 'Unexpected operator: ' + values[1]

    @visit_children_decor
    def concat_expr(self, values):
        '''
        evaluate a concatenation expression
        '''
        v_1 = convert_str(values[0])
        v_2 = convert_str(values[1])
        if isinstance(v_1, CellError):
            return v_1
        if isinstance(v_2, CellError):
            return v_2
        return v_1 + v_2

    @visit_children_decor
    def unary_op(self, values):
        '''
        calculate positive or negative value of given Decimal
        '''
        val = check_arithmetic_input(values[1])
        if isinstance(val, CellError):
            return val
        if values[0] == '+':
            return val
        if values[0] == '-':
            return 0 - val
        assert False, 'Unexpected operator: ' + values[0]

    @visit_children_decor
    def compare_expr(self, values):
        '''
        Evaluate a comparison expression
        '''
        if values[0] is None and values[2] is None:
            values[0] = decimal.Decimal()
            values[2] = decimal.Decimal()
        if values[0] is None:
            values[0] = _COMPARISON_EMPTY_CELL[type(values[2])]
        if values[2] is None:
            values[2] = _COMPARISON_EMPTY_CELL[type(values[0])]
        operator = _COMPARISON_LAMBDAS[values[1]]
        return compare_op(values[0], values[2], operator)

    def function(self, tree):
        '''
        Evaluate a function
        '''
        function_name = tree.children[0]
        custom_function = DICTIONARY_FUNCTIONS.get(function_name)
        if custom_function is None:
            detail = "Function name is not recognized"
            return CellError(CellErrorType.BAD_NAME, detail)
        custom_func, dynamic_dep = custom_function
        if not dynamic_dep:
            return custom_func(self, tree.children[1:])
        self.workbook.clear_dynamic(self.this_cell)
        add_dynamic = self.workbook.add_dynamic_dep
        add_dep = AddDependencies(add_dynamic, self.sheet, self.this_cell)
        return custom_func(self, add_dep, tree.children[1:])

    def error(self, tree):
        '''
        return CellError value
        '''
        error = str_to_error(tree.children[0].upper())
        return CellError(error, tree.children[0].upper())

    def number(self, tree):
        '''
        return Decimal value of parsed number
        '''
        num = tree.children[0]
        if '.' in num:
            num = num.rstrip('0').rstrip('.')
        return decimal.Decimal(num)

    def boolean(self, tree):
        '''
        Return Boolean value
        '''
        return tree.children[0].upper() == 'TRUE'

    def string(self, tree):
        '''
        return parsed string with quotes removed
        '''
        return tree.children[0].value[1:-1]

    def parens(self, tree):
        '''
        return contents within parentheses
        '''
        return self.visit(tree.children[0])

    def cell(self, tree):
        '''
        return value of cell refrenced in formula
        '''
        try:
            if len(tree.children) == 1:
                cellref = tree.children[0].replace('$', '').upper()
                sheetref = self.sheet.upper()
                cell_val = self.workbook.sheets[sheetref][cellref].get_value()
            else:
                sheet_name = tree.children[0]
                if sheet_name[0] == '\'':
                    sheet_name = sheet_name[1:-1]
                cellref = tree.children[1].replace('$', '').upper()
                sheetref = sheet_name.upper()
                cell_val = self.workbook.sheets[sheetref][cellref].get_value()
            return cell_val
        except KeyError:
            detail = 'Bad reference to non-existent sheet: '+sheet_name
            return CellError(CellErrorType.BAD_REFERENCE, detail)

def sheetname_manipulator(old_and_new, values):
    '''
    replace sheet names referenced in cell contents
    '''
    old_name = old_and_new[0]
    new_name = old_and_new[1]
    if len(values) == 1:
        return values[0]
    sheet_name = values[0].strip('\'')
    if sheet_name.upper() == old_name.upper():
        sheet_name = new_name
    if not set(sheet_name).isdisjoint(_REQUIRE_QUOTES):
        return '\''+sheet_name+'\''+'!'+values[1]
    return sheet_name+'!'+values[1]

def cellref_manipulator(args, values):
    '''
    return given cell reference with necessary locations replaced
    '''
    workbook = args[0]
    x_diff = args[1]
    y_diff = args[2]
    new_sheet_name = args[3]
    if len(values) == 1:
        if values[0][0] == '$':
            x_diff = 0
            values[0] = values[0][1:]
        if values[0].find('$') > 0:
            y_diff = 0
        cellref = values[0].replace('$', '')
        row, col = workbook.loc_to_tuple(cellref)
        return workbook.tuple_to_loc(row + x_diff, col + y_diff)
    if values[1][0] == '$':
        x_diff = 0
        values[0] = values[0][1:]
    if values[1].find('$'):
        y_diff = 0
    cellref = values[1].replace('$', '')
    row, col = workbook.loc_to_tuple(cellref)
    if new_sheet_name is not None:
        new_loc = workbook.tuple_to_loc(row + x_diff, col + y_diff)
        return new_sheet_name +'!'+ new_loc
    return values[0]+'!'+ workbook.tuple_to_loc(row + x_diff, col + y_diff)

class ContentManipulation(lark.Transformer):
    '''
    replace sheet names referenced in cell contents
    '''
    def __init__(self, manipulation_type, args):
        super().__init__()
        self.manipulator = manipulation_type
        self.args = args

    def add_expr(self, values):
        '''
        return given addition expression formatted with added spaces
        '''
        return values[0]+' '+values[1]+' '+values[2]

    def mul_expr(self, values):
        '''
        return given multiplication expression formatted with added spaces
        '''
        return values[0]+' '+values[1]+' '+values[2]

    def concat_expr(self, values):
        '''
        return given concatenation expression formatted with added spaces
        '''
        return values[0]+' '+'&'+' '+values[1]

    def unary_op(self, values):
        '''
        return given unary expression formatted with added spaces
        '''
        return values[0] + values[1]

    def error(self, values):
        '''
        return given error string
        '''
        return values[0]

    def number(self, values):
        '''
        return given number
        '''
        return values[0]

    def string(self, values):
        '''
        return given string
        '''
        return values[0]

    def parens(self, values):
        '''
        return formatted given parenthetical expression
        '''
        return '('+values[0]+')'

    def function(self, values):
        '''
        return formatted given function expression
        '''
        func_string = values[0]+'('
        for val in values[1:]:
            if val is None:
                break
            func_string += val + ','
        return func_string.rstrip(',') +')'

    def cell(self, values):
        '''
        return given cell reference with necessary sheet names replaced
        '''
        return self.manipulator(self.args, values)
