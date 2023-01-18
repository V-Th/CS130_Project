#!/usr/bin/env python3
from .cell import _Cell
from .cellerror import *
from .cellgraph import _CellGraph
import lark
import logging

class Workbook():
    def __init__(self):
        self.workbook = self
        self._sheets = {}
        self._extents = {}
        self._graph = _CellGraph()
        self._display_sheets = {}

    def num_sheets(self) -> int:
        return len(self._sheets)

    def list_sheets(self) -> list[str]:
        return self._sheets.keys()
    
    def __list_cells(self, sheet_name) -> list[str]:
        return self._sheets[sheet_name].keys()
    
    def _sheet_name_exists(self, sheet_name: str) -> bool:
        return sheet_name.upper() in (s.upper() for s in self._sheets.keys())
    
    def _location_exists(self, sheet_name:str, location: str) -> bool:
        return location.upper() in (l.upper() for l in self._sheets[sheet_name.upper()].keys())
    
    # returns false if given sheet name has leading or trailing whitespace, already exists in the workbook, 
    # or contains an illegal character 
    # true otherwise
    def _is_valid_sheet(self, sheet_name) -> bool:
        if not isinstance(sheet_name, str):
            return False
        if self._sheet_name_exists(sheet_name):
            logging.info("Workbook: is_valid_sheet: sheet name already exists")
            return False
        if (sheet_name.strip() != sheet_name):
            logging.info("Workbook: is_valid_sheet: leading or trailing whitespace")
            return False
        if ('/' in sheet_name) or ('<' in sheet_name) or ('=' in sheet_name) or ('>' in sheet_name) or ('[' in sheet_name) or (']' in sheet_name) or ('+' in sheet_name):
            logging.info("Workbook: is_valid_sheet: illegal charcter in sheet name")
            return False
        return True
    
    # returns whether the given string represents a valid location in the sheet
    def _is_valid_location(self, location: str) -> bool:
        if len(location) > 8 or len(location) < 2:
            logging.info("Workbook: is_valid_location: invalid cell location, too long or too short")
            return False
        parser = lark.Lark.open('formulas.lark', rel_to=__file__, start='expression')
        try:
            tree = parser.parse(location)
            return True
        except:
            print("Workbook: is_valid_location: could not recognize cell reference")
            return False 
    
    # creates new empty spreadsheet if the given sheet_name is valid 
    # returns a the index and name of the new spreadsheet
    def new_sheet(self, sheet_name: str = None) -> tuple[int, str]:
        if self._is_valid_sheet(sheet_name):
            self._sheets[sheet_name.upper()] = {}
            return (self.num_sheets(), sheet_name)
        else:
            n = 1
            while(True):
                if "SHEET" + str(n) not in self._sheets and n <= self.num_sheets() + 1:
                    self._sheets["SHEET" + str(n)] = {}
                    self._display_sheets["SHEET" + str(n)] = "Sheet" + str(n)
                    return (n, "Sheet" + str(n))
                n += 1

    # delete the given spreadsheet            
    def del_sheet(self, sheet_name: str) -> None:
        if self._sheet_name_exists(sheet_name):
            self._sheets.pop(sheet_name.upper())

    # return number of rows and columns in the given spreadsheet
    def get_sheet_extent(self, sheet_name: str) -> tuple[int, int]:
        if self._sheet_name_exists(sheet_name):
            return self._extents[sheet_name.upper()]
        logging.info("Workbook: get_sheet_extent: sheet name not in extents")
        return None
    
    # when a spreadsheet is added or deleted, update the extent of that sheet 
    def __update_sheet_extent(self, sheet_name: str) -> None:
        if self._sheet_name_exists(sheet_name):
            a = 0
            b = 0
            new_extent = (0,0)
            n = 0
            for i in self._sheets[sheet_name.upper()].keys():
                for j in range(len(i)):
                    if i[j].upper().isalpha():
                        a += ord(i[j].upper()) - 64 + (26 * n)
                    else:
                        b = int(i[j:]) 
                        break
                if (a,b) > new_extent:
                    new_extent = (a,b)
            self._extents[sheet_name.upper()] = new_extent
    
    # set the cell of the given location to the given contents
    # return true if successful, false otherwise
    def set_cell_contents(self, sheet_name: str, location: str, contents:str) -> None:
        if not self._sheet_name_exists(sheet_name):
            return False
        if not self._is_valid_location(location):
            return False
        # check if the sheet already has a cell, if not create one
        if not self._location_exists(sheet_name, location):
            self._sheets[sheet_name.upper()][location.upper()] = _Cell(self.workbook, sheet_name, location)
        # if the sheet already has the cell, remove its edges from graph
        else:
            self._graph.remove_node(self._sheets[sheet_name.upper()][location.upper()])
        # update the cell contents
        self._sheets[sheet_name.upper()][location.upper()].set_contents(contents)
        self.__update_sheet_extent(sheet_name.upper())
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
        self._graph.SCC()
        # for those in SCC sets with other, set CIRCREF error
        for set in self._graph.setList:
            if len(set) == 1:
                continue
            for i in set:
                cell_sheet = i.sheet_name.upper()
                cell_loc = i.location.upper()
                self._sheets[cell_sheet][cell_loc].value = CellError("#CIRCREF!", "Circular reference detected")
        return
    
    # return the contents of the cell at the given location
    def get_cell_contents(self, sheet_name: str, location: str):
        if self._sheet_name_exists(sheet_name) and self._location_exists(sheet_name, location):
            return self._sheets[sheet_name.upper()][location.upper()].get_contents()
        return None

    # return the value of the cell at the given location    
    def get_cell_value(self, sheet_name: str, location: str):
        # parameter validation
        if not self._sheet_name_exists(sheet_name):
            logging.info("Workbook: get_cell_value: sheet_name does not exist")
            return None
        if not self._location_exists(sheet_name, location):
            logging.info("Workbook: get_cell_value: location does not exist")
            return None
        return self._sheets[sheet_name.upper()][location.upper()].get_value()
    
    def get_dependent_cell_value(self, sheet_name:str, location:str):
        return self._sheets[sheet_name.upper()][location.upper()].value
