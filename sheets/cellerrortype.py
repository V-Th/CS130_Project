'''
This module implements the cell error types and functionality that may be
needed by the internals of the workbook.
'''
from enum import Enum

class CellErrorType(Enum):
    '''
    This class implements the several types of errors that can occur in a
    workbook.
    '''
    PARSE_ERROR = 1

    CIRCULAR_REFERENCE = 2

    BAD_REFERENCE = 3

    BAD_NAME = 4

    TYPE_ERROR = 5

    DIVIDE_BY_ZERO = 6

_STR_ERROR = {
    "#ERROR!": CellErrorType.PARSE_ERROR,
    "#CIRCREF!": CellErrorType.CIRCULAR_REFERENCE,
    "#REF!": CellErrorType.BAD_REFERENCE,
    "#NAME?": CellErrorType.BAD_NAME,
    "#VALUE!": CellErrorType.TYPE_ERROR,
    "#DIV/0!": CellErrorType.DIVIDE_BY_ZERO
}

_ERROR_STR = {
    CellErrorType.PARSE_ERROR: "#ERROR!",
    CellErrorType.CIRCULAR_REFERENCE: "#CIRCREF!",
    CellErrorType.BAD_REFERENCE: "#REF!",
    CellErrorType.BAD_NAME: "#NAME?",
    CellErrorType.TYPE_ERROR: "#VALUE!",
    CellErrorType.DIVIDE_BY_ZERO: "#DIV/0!"
}

def error_to_str(str_error):
    '''
    Converts an error to its message string.
    '''
    if str_error in _ERROR_STR:
        return _ERROR_STR[str_error]
    return None

def str_to_error(error_str):
    '''
    Converts a message string to its error.
    '''
    if error_str in _STR_ERROR:
        return _STR_ERROR[error_str]
    return None
