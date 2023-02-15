'''
This module implements a workbook alongside its errors and errortypes.
'''
from .workbook import Workbook
from .cellerror import CellError
from .cellerrortype import CellErrorType

# pylint: disable=C0103
version = 1.2

__all__ = ["Workbook", "CellError", "CellErrorType"]
