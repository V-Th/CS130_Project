'''
This module implements the different cell errors possible in the workbook.
'''
from typing import Optional
from .cellerrortype import CellErrorType

class CellError:
    '''
    This class implements the cell error structure.

    Error_type is from the 6 different errortypes from cellerrortype.
    Details is a message string attached to the error.
    Exception is the exception that created the error.
    '''
    def __init__(self, error_type: CellErrorType, detail: str,
                 exception: Optional[Exception] = None):
        self._error_type = error_type
        self._detail = detail
        self._exception = exception

    def get_type(self) -> CellErrorType:
        '''
        Returns the error type.
        '''
        return self._error_type

    def get_detail(self) -> str:
        '''
        Returns the error message from the error.
        '''
        return self._detail

    def get_exception(self) -> Optional[Exception]:
        '''
        Returns the exception that created the error.
        '''
        return self._exception

    def __str__(self) -> str:
        return f'ERROR[{self._error_type}, "{self._detail}"]'

    def __repr__(self) -> str:
        return self.__str__()
