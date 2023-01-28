#!/usr/bin/env python3
from .cell import _Cell
from .cellerror import *
from .cellgraph import _CellGraph
import lark
import string
import logging

_SHEET_CHARS = set(" .?!,:;!@#$%^&*()-_"+string.ascii_letters+string.digits)

class Workbook():
    def __init__(self):
        self.workbook = self
        self._sheets = {}
        self._extents = {}
        self._display_sheets = {}
        self._graph = _CellGraph()

    def num_sheets(self) -> int:
        return len(self._sheets)

    def list_sheets(self) -> list[str]:
        return [name for name in self._display_sheets.values()]
    
    def _sheet_name_exists(self, sheet_name: str) -> bool:
        return sheet_name.upper() in (s.upper() for s in self._sheets.keys())
    
    def _location_exists(self, sheet_name:str, loc: str) -> bool:
        cells = (c.upper() for c in self._sheets[sheet_name.upper()].keys())
        return loc.upper() in cells
    
    # returns false if given sheet name has leading or trailing whitespace,
    # already exists in the workbook, or contains an illegal character true
    # otherwise
    def _is_valid_sheet(self, sheet_name) -> bool:
        if not isinstance(sheet_name, str):
            return False
        if self._sheet_name_exists(sheet_name):
            logging.info("Workbook: is_valid_sheet: sheet name already exists")
            return False
        if not sheet_name:
            logging.info("Workbook: is_valid_sheet: empty string")
            return False
        if (sheet_name.strip() != sheet_name):
            logging.info("Workbook: is_valid_sheet: leading or trailing whitespace")
            return False
        if not set(sheet_name).issubset(_SHEET_CHARS):
            logging.info("Workbook: is_valid_sheet: illegal charcter in sheet name")
            return False
        return True

    def _loc_to_tuple(self, loc: str):
        a, b = 0, 0
        for i, char in enumerate(loc):
            if char.upper().isalpha():
                a = (a * 26) + (ord(char.upper()) - ord('A') + 1) 
            else:
                b = int(loc[i:])
                break
        return (a, b)
    
    # returns whether the given string represents a valid location in the sheet
    def _is_valid_location(self, location: str) -> bool:
        if len(location) > 8 or len(location) < 2:
            logging.info("Workbook: is_valid_location: invalid cell location, too long or too short")
            return False
        parser = lark.Lark.open('formulas.lark', rel_to=__file__, start='expression')
        try:
            parser.parse(location)
        except:
            logging.info("Workbook: is_valid_location: could not recognize cell reference")
            return False 
        # check that location is within limits A-ZZZZ and 1-9999
        a, b = self._loc_to_tuple(location)
        if a > 475254 or b > 9999:
            return False
        return True
    
    # creates new empty spreadsheet if the given sheet_name is valid 
    # returns a the index and name of the new spreadsheet
    def new_sheet(self, sheet_name: str = None) -> tuple[int, str]:
        if sheet_name is None:
            n = 1
            while(self._sheet_name_exists("Sheet" + str(n))):
                n += 1
            sheet_name = "Sheet" + str(n)
        elif not self._is_valid_sheet(sheet_name):
            raise ValueError
        self._sheets[sheet_name.upper()] = {}
        self._display_sheets[sheet_name.upper()] = sheet_name
        self._update_sheet_extent(sheet_name.upper())
        return (self.num_sheets(), sheet_name)

    # delete the given spreadsheet            
    def del_sheet(self, sheet_name: str) -> None:
        if self._sheet_name_exists(sheet_name):
            dead_sheet = self._sheets.pop(sheet_name.upper())
            self._display_sheets.pop(sheet_name.upper())
            for cells in dead_sheet.values():
                cells.set_contents(None)
        else:
            raise KeyError

    # return number of rows and columns in the given spreadsheet
    def get_sheet_extent(self, sheet_name: str) -> tuple[int, int]:
        if self._sheet_name_exists(sheet_name):
            return self._extents[sheet_name.upper()]
        else:
            raise KeyError
    
    # when a spreadsheet is added or deleted, update the extent of that sheet 
    def _update_sheet_extent(self, sheet_name: str) -> None:
        if not self._sheet_name_exists(sheet_name):
            return
        max_a, max_b = 0, 0
        for loc in self._sheets[sheet_name.upper()].keys():
            if self.get_cell_contents(sheet_name, loc) is None:
                continue
            a, b = self._loc_to_tuple(loc)
            if a > max_a:
                max_a = a
            if b > max_b:
                max_b = b
        self._extents[sheet_name.upper()] = (max_a, max_b)

    # Update the cellgraph and check for loops
    def _check_for_loop(self):
        self._graph.SCC()
        # for those in SCC sets with other, set CIRCREF error
        for set in self._graph.setList:
            if len(set) == 1:
                for node in set:
                    if node in self._graph.graph[node]:
                        node.value = CellError(CellErrorType("#CIRCREF!"), "Circular reference detected")
                continue
            for i in set:
                cell_sheet = i.sheet_name.upper()
                cell_loc = i.location.upper()
                cell_err = CellError(CellErrorType("#CIRCREF!"), "Circular reference detected")
                self._sheets[cell_sheet][cell_loc].value = cell_err
        return
    
    # set the cell of the given location to the given contents
    # return true if successful, false otherwise
    def set_cell_contents(self, sheet_name: str, location: str, contents:str) -> None:
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_location(location):
            raise ValueError
        # check if the sheet already has a cell, if not create one
        if not self._location_exists(sheet_name, location):
            self._sheets[sheet_name.upper()][location.upper()] = _Cell(self.workbook, sheet_name, location)
        else:
            self._graph.remove_node(self._sheets[sheet_name.upper()][location.upper()])
        # update the cell contents
        self._sheets[sheet_name.upper()][location.upper()].set_contents(contents)
        self._check_for_loop()
        ref_cells = []
        self._graph.dfs_nodes([self._sheets[sheet_name.upper()][location.upper()]], ref_cells)
        for cell in ref_cells:
            cell.update_value()
        self._update_sheet_extent(sheet_name.upper())
        return

    # return the cell object at a particular location
    def add_dependency(self, src_cell: _Cell, location: str, sheet_name: str) -> None:
        assert self._sheet_name_exists(sheet_name)
        assert self._is_valid_location(location.upper())
        # check if the sheet already has a cell, if not create one
        if not self._location_exists(sheet_name, location):
            self._sheets[sheet_name.upper()][location.upper()] = _Cell(self.workbook, sheet_name, location)
        dest_cell = self._sheets[sheet_name.upper()][location.upper()]
        self._graph.add_edge(src_cell, dest_cell)
        # check for strongly connected component set
        self._check_for_loop()
    
    # return the contents of the cell at the given location
    def get_cell_contents(self, sheet_name: str, location: str):
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_location(location):
            raise ValueError
        return self._sheets[sheet_name.upper()][location.upper()].get_contents()

    # return the value of the cell at the given location    
    def get_cell_value(self, sheet_name: str, location: str):
        # parameter validation
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_location(location):
            raise ValueError
        if not self._location_exists(sheet_name, location):
            self._sheets[sheet_name.upper()][location.upper()] = _Cell(self.workbook, sheet_name, location)
        return self._sheets[sheet_name.upper()][location.upper()].get_value()
