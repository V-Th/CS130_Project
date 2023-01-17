from .cellerrortype import CellErrorType
from typing import Optional

class CellError:
    def __init__(self, error_type: CellErrorType, detail: str,
                 exception: Optional[Exception] = None):
        self._error_type = error_type
        self._detail = detail
        self._exception = exception

    def get_type(self) -> CellErrorType:
        return self._error_type

    def get_detail(self) -> str:
        return self._detail

    def get_exception(self) -> Optional[Exception]:
            return self._exception

    def __str__(self) -> str:
        return f'ERROR[{self._error_type}, "{self._detail}"]'

    def __repr__(self) -> str:
        return self.__str__()