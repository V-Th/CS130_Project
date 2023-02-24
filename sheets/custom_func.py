'''
The functions module implements function calls with many arguments or none
'''
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

# Dictionary of Function Calls
DICTIONARY_FUNCTIONS = {
    "AND": func_and,
    "OR": func_or,
    "NOT": func_not,
    "XOR": func_xor
}
