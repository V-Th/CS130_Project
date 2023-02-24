'''
The functions module implements function calls with many arguments or none
'''
import lark
import sheets
from sheets import cell
from .cellerror import CellError
from .cellerrortype import CellErrorType

def check_boolean_input(value):
    '''
    Performs implicit conversions to boolean or returns type error
    '''
    if isinstance(value, (bool, CellError)):
        return value
    if value is None:
        return False
    if isinstance(value, str):
        if value.upper() == "TRUE":
            return True
        if value.upper() == "FALSE":
            return False
        detail = "String cannot be converted to Boolean"
        return CellError(CellErrorType(5), detail)
    return bool(value)

def func_and(evaluator, args):
    '''
    Function to perform boolean AND logic
    '''
    if args[0] is None:
        detail = "Not enough arguments for AND"
        return CellError(CellErrorType(5), detail)
    for arg in args:
        val = evaluator.visit(arg)
        check = check_boolean_input(val)
        if isinstance(check, CellError):
            return check
        if not check:
            return False
    return True

def func_or(evaluator, args):
    '''
    Function to perform boolean OR logic
    '''
    if args[0] is None:
        detail = "Not enough arguments for OR"
        return CellError(CellErrorType(5), detail)
    for arg in args:
        val = evaluator.visit(arg)
        check = check_boolean_input(val)
        if isinstance(check, CellError):
            return check
        if check:
            return True
    return False

def func_not(evaluator, arg):
    '''
    Function to perform boolean OR logic
    '''
    if arg[0] is None:
        detail = "Not enough arguments for NOT"
        return CellError(CellErrorType(5), detail)
    if len(arg) > 1:
        detail = "Too many arguments for NOT"
        return CellError(CellErrorType(5), detail)
    val = evaluator.visit(arg[0])
    check = check_boolean_input(val)
    if isinstance(check, CellError):
        return check
    return not check

def func_xor(evaluator, args):
    '''
    Function to perform boolean XOR logic
    '''
    if args[0] is None:
        detail = "Not enough arguments for XOR"
        return CellError(CellErrorType(5), detail)
    return_bool = False
    for arg in args:
        val = evaluator.visit(arg)
        check = check_boolean_input(val)
        if isinstance(check, CellError):
            return check
        if check:
            return_bool = not return_bool
    return return_bool

def func_exact(evaluator, args):
    '''
    Function that compares two strings
    '''
    if len(args) < 2:
        detail = "Not enough arguments for EXACT"
        return CellError(CellErrorType(5), detail)
    if len(args) > 2:
        detail = "Too many arguments for NOT"
        return CellError(CellErrorType(5), detail)
    v_1 = cell.convert_str(evaluator.visit(args[0]))
    v_2 = cell.convert_str(evaluator.visit(args[1]))
    return v_1 == v_2

def func_if(evaluator, add_dep, args):
    '''
    Function that evaluates the condition and the corresponding event

    The condition should be evaluated before any of the values.
    Then, the first value should be evaluated if the condition is true.
    The second value does not need to be evaluated if the first value is
    valid. Similarly, if the condition is false then the first value does not
    need to be evaluated at all.
    '''
    if len(args) < 2:
        detail = "Not enough arguments for IF"
        return CellError(CellErrorType(5), detail)
    if len(args) > 3:
        detail = "Too many arguments for IF"
        return CellError(CellErrorType(5), detail)
    cond = evaluator.visit(args[0])
    if isinstance(cond, CellError):
        return cond
    if cond:
        add_dep.visit(args[1])
        return evaluator.visit(args[1])
    if len(args) == 3:
        add_dep.visit(args[2])
        return evaluator.visit(args[2])
    return False

def func_iferror(evaluator, add_dep, args):
    '''
    Function that evaluates the first value and then the second if it is an
    error

    The first value is evaluated and returned if it is not an error. If it is
    an error, then the second value is evaluated and returned. If no second
    value is specified then a empty string is returned.
    '''
    if args[0] is None:
        detail = "Not enough arguments for IFERROR"
        return CellError(CellErrorType(5), detail)
    if len(args) > 2:
        detail = "Too many arguments for IFERROR"
        return CellError(CellErrorType(5), detail)
    val1 = evaluator.visit(args[0])
    if not isinstance(val1, CellError):
        return val1
    if len(args) == 2:
        add_dep.visit(args[1])
        return evaluator.visit(args[1])
    return ""

def func_choose(evaluator, add_dep, args):
    '''
    Function that evaluates the value for a given index

    Only the value specified by the value should be evaluated and considered
    by the cellgraph
    '''
    if len(args) < 2:
        detail = "Not enough arguments for CHOOSE"
        return CellError(CellErrorType.TYPE_ERROR, detail)
    index = evaluator.visit(args[0])
    if index == 0 or index > len(args):
        detail = "The index is out of bounds"
        return CellError(CellErrorType.TYPE_ERROR, detail)
    add_dep.visit(args[index])
    return evaluator.visit(args[index])

def func_isblank(evaluator, args):
    '''
    Function that returns True if value is empty-cell value and False
    otherwise

    Note: The representation of empty-cell values is None
    '''
    if len(args) > 1:
        detail = "Too many arguments for ISBLANK"
        return CellError(CellErrorType.TYPE_ERROR, detail)
    if args[0] is None:
        detail = "Not enough arguments for ISBLANK"
        return CellError(CellErrorType.TYPE_ERROR, detail)
    value = evaluator.visit(args[0])
    return value is None

def func_iserror(evaluator, args):
    '''
    Function that returns True if value is empty-cell value and False
    otherwise

    Note: The representation of empty-cell values is None
    '''
    if len(args) > 1:
        detail = "Too many arguments for ISBLANK"
        return CellError(CellErrorType.TYPE_ERROR, detail)
    if args[0] is None:
        detail = "Not enough arguments for ISBLANK"
        return CellError(CellErrorType.TYPE_ERROR, detail)
    value = evaluator.visit(args[0])
    return isinstance(value, CellError)

def func_version(_, args):
    '''
    Returns the version of the sheets library
    '''
    if args[0] is not None:
        detail = "VERSION takes no arguments"
        return CellError(CellErrorType.TYPE_ERROR, detail)
    return sheets.version

def func_indirect(evaluator, add_dep, args):
    '''
    Function that parses a string into a cell reference and returns the cell's
    value
    '''
    if len(args) > 1:
        detail = "Too many arguments for INDIRECT"
        return CellError(CellErrorType.TYPE_ERROR, detail)
    if args[0] is None:
        detail = "Not enough arguments for INDIRECT"
        return CellError(CellErrorType.TYPE_ERROR, detail)
    cellref_str = cell.convert_str(evaluator.visit(args))
    try:
        cellref = cell.parser.parse('=' + cellref_str)
    # The TypeError catches instances where the cellref_str is an error
    except (lark.exceptions.LarkError, TypeError):
        detail = "String is not a valid cell-reference"
        return CellError(CellErrorType.BAD_REFERENCE, detail)
    add_dep.visit(cellref)
    return evaluator.visit(cellref)

# Dictionary of Function Calls
# The boolean stores whether the function will need dynamic dependencies
DICTIONARY_FUNCTIONS = {
    "AND": (func_and, False),
    "OR": (func_or, False),
    "NOT": (func_not, False),
    "XOR": (func_xor, False),
    "EXACT": (func_exact, False),
    "IF": (func_if, True),
    "IFERROR": (func_iferror, True),
    "CHOOSE": (func_choose, True),
    "ISBLANK": (func_isblank, False),
    "ISERROR": (func_iserror, False),
    "VERSION": (func_version, False),
    "INDIRECT": (func_indirect, True)
}
