#!/usr/bin/env python3
from cell import *
from cellerror import *
from cellgraph import *
import lark
import logging

class Workbook():
    def __init__(self):
        self.workbook = self
        self.sheets = {}
        self.extents = {}
        self.graph = CellGraph()
        self.display_sheets = {}

    def num_sheets(self) -> int:
        return len(self.sheets)

    def list_sheets(self) -> list[str]:
        return self.sheets.keys()
    
    def __list_cells(self, sheet_name) -> list[str]:
        return self.sheets[sheet_name].keys()
    
    def sheet_name_exists(self, sheet_name: str) -> bool:
        return sheet_name.upper() in (s.upper() for s in self.sheets.keys())
    
    def location_exists(self, sheet_name:str, location: str) -> bool:
        return location.upper() in (l.upper() for l in self.sheets[sheet_name.upper()].keys())
    
    # returns false if given sheet name has leading or trailing whitespace, already exists in the workbook, 
    # or contains an illegal character 
    # true otherwise
    def is_valid_sheet(self, sheet_name) -> bool:
        if type(sheet_name) != 'str':
            return False
        if self.sheet_name_exists(sheet_name):
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
    def is_valid_location(self, location: str) -> bool:
        if len(location) > 8 or len(location) < 2:
            logging.info("Workbook: is_valid_location: invalid cell location, too long or too short")
            return False
        parser = lark.Lark.open('formulas.lark', rel_to=__file__, start='expression')
        try:
            tree = parser.parse(location)
        except:
            print("Workbook: is_valid_location: could not recognize cell reference")
            return False 
        # check that location is within limits A-ZZZZ and 1-9999
        a, b = 0, 0
        for i in range(len(location)):
            if location[i].upper().isalpha():
                a = (a * 26) + (ord(location[i].upper()) - ord('A') + 1) 
            else:
                b = int(location[i:]) 
                break
        if a > 475254 or b > 9999:
            return False
        return True
    
    # creates new empty spreadsheet if the given sheet_name is valid 
    # returns a the index and name of the new spreadsheet
    def new_sheet(self, sheet_name:str = None) -> tuple[int, str]:
        if sheet_name == None:
            n = 1
            while(True):
                if "SHEET" + str(n) not in self.sheets and n <= self.num_sheets() + 1:
                    self.sheets["SHEET" + str(n)] = {}
                    self.display_sheets["SHEET" + str(n)] = "Sheet" + str(n)
                    return (n, "Sheet" + str(n))
                n += 1

        elif self.is_valid_sheet(sheet_name):
            self.sheets[sheet_name.upper()] = {}
            self.display_sheets[sheet_name.upper()] = sheet_name
            return (self.num_sheets(), sheet_name)
        
        else:
            logging.info(f"Workbook: new_sheet: {sheet_name} is invalid sheet name")

    # delete the given spreadsheet            
    def del_sheet(self, sheet_name: str) -> None:
        if self.sheet_name_exists(sheet_name):
            self.sheets.pop(sheet_name.upper())
            self.display_sheets.pop(sheet_name.upper())

    # return number of rows and columns in the given spreadsheet
    def get_sheet_extent(self, sheet_name: str) -> tuple[int, int]:
        if self.sheet_name_exists(sheet_name):
            return self.extents[sheet_name.upper()]
        logging.info("Workbook: get_sheet_extent: sheet name not in extents")
        return None
    
    # when a spreadsheet is added or deleted, update the extent of that sheet 
    def __update_sheet_extent(self, sheet_name: str) -> None:
        if self.sheet_name_exists(sheet_name):
            max_a, max_b = 0, 0
            for i in self.sheets[sheet_name.upper()].keys():
                a, b = 0, 0
                for j in range(len(i)):
                    if i[j].upper().isalpha():
                        a = (a * 26) + (ord(i[j].upper()) - ord('A') + 1) 
                    else:
                        b = int(i[j:]) 
                        break
                if a > max_a:
                    max_a = a
                if b > max_b:
                    max_b = b
            self.extents[sheet_name.upper()] = (max_a, max_b)
    
    # set the cell of the given location to the given contents
    # return true if successful, false otherwise
    def set_cell_contents(self, sheet_name: str, location: str, contents:str) -> None:
        if not self.sheet_name_exists(sheet_name):
            return False
        if not self.is_valid_location(location):
            return False
        # check if the sheet already has a cell, if not create one
        if not self.location_exists(sheet_name, location):
            self.sheets[sheet_name.upper()][location.upper()] = Cell(self.workbook, sheet_name, location, self.graph)
        # update the cell contents
        self.sheets[sheet_name.upper()][location.upper()].set_contents(contents)
        self.__update_sheet_extent(sheet_name.upper())
        return

    # return the cell object at a particular location
    def add_dependency(self, src_cell: Cell, location: str, sheet_name: str) -> Cell:
        assert self.sheet_name_exists(sheet_name), sheet_name
        assert self.is_valid_location(location.upper())
        # check if the sheet already has a cell, if not create one
        if not self.location_exists(sheet_name, location):
            self.sheets[sheet_name.upper()][location.upper()] = Cell(self.workbook, sheet_name, location, self.graph)
        dest_cell = self.sheets[sheet_name.upper()][location.upper()]
        self.graph.add_edge(src_cell, dest_cell)
        return dest_cell
    
    # return the contents of the cell at the given location
    def get_cell_contents(self, sheet_name: str, location: str):
        if self.sheet_name_exists(sheet_name) and self.location_exists(sheet_name, location):
            return self.sheets[sheet_name.upper()][location.upper()].get_contents()
        return None

    # return the value of the cell at the given location    
    def get_cell_value(self, sheet_name: str, location: str):
        # parameter validation
        if not self.sheet_name_exists(sheet_name):
            logging.info("Workbook: get_cell_value: sheet_name does not exist")
            return None
        if not self.location_exists(sheet_name, location):
            logging.info("Workbook: get_cell_value: location does not exist")
            return None
        # get strongly connected component set
        self.graph.SCC()
        # get values in order of the strongly connected set
        for set in self.graph.setList:
            if len(set) > 1:
                return CellError("#CIRCREF!", "Circular reference detected")
            for j in set:
                self.sheets[j.sheet_name.upper()][j.location.upper()].get_value()
        return self.sheets[sheet_name.upper()][location.upper()].get_value()
    
    def get_dependent_cell_value(self, sheet_name:str, location:str):
        return self.sheets[sheet_name.upper()][location.upper()].value
