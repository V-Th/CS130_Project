from enum import Enum

class CellErrorType(Enum):
    PARSE_ERROR = "#ERROR!"

    CIRCULAR_REFERENCE = "#CIRCREF!"
    
    BAD_REFERENCE = "#REF!"
    
    BAD_NAME = "#NAME?"
    
    TYPE_ERROR = "#VALUE!"
    
    DIVIDE_BY_ZERO = "#DIV/0!"

