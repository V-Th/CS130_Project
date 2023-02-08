from enum import Enum

class CellErrorType(Enum):
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
    return _ERROR_STR[str_error]

def str_to_error(error_str):
    return _STR_ERROR[error_str]
