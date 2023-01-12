#!/usr/bin/env python3
#from sheet import *
from cell import * 
from cell_graph import *
import decimal
import lark

class Workbook():
    def __init__(self):
        self.workbook = self
        self.sheets = {}
        self.extents = {}
        self.graph = CellGraph()

    def num_sheets(self) -> int:
        return len(self.sheets)

    def list_sheets(self) -> list[str]:
        return self.sheets.keys()
    
    def list_cells(self, sheet_name) -> list[str]:
        return self.sheets[sheet_name].keys()
    
    # returns false if given sheet name has leading or trailing whitespace, already exists in the workbook, 
    # or contains an illegal character 
    # true otherwise
    def is_valid_sheet(self, sheet_name: str) -> bool:
        if (sheet_name.strip() != sheet_name) or (sheet_name in self.sheets):
            return False
        if ('/' in sheet_name) or ('<' in sheet_name) or ('=' in sheet_name) or ('>' in sheet_name) or ('[' in sheet_name) or (']' in sheet_name) or ('+' in sheet_name):
            return False
        return True
    
    # returns whether the given string represents a valid location in the sheet
    def is_valid_location(self, location: str) -> bool:
        if len(location) > 8 or len(location) < 2:
            return False
        parser = lark.Lark.open('formulas.lark', start='expression')
        try:
            tree = parser.parse(location)
            return True
        except:
            return False 
    
    # creates new empty spreadsheet if the given sheet_name is valid 
    # returns a the index and name of the new spreadsheet
    def new_sheet(self, sheet_name:str = None) -> tuple[int, str]:
        if self.is_valid_sheet(sheet_name):
            self.sheets[sheet_name] = {}
            return (self.num_sheets(), sheet_name)
        else:
            n = 1
            while(True):
                if "SHEET" + str(n) not in self.sheets and n <= self.num_sheets():
                    self.sheets["SHEET" + str(n)] = {}
                    return (n, "SHEET" + str(n))
                n += 1

    # delete the given spreadsheet            
    def del_sheet(self, sheet_name: str) -> None:
        if sheet_name in self.sheets:
            self.sheets.pop(sheet_name)

    # return number of rows and columns in the given spreadsheet
    def get_sheet_extent(self, sheet_name: str) -> tuple[int, int]:
        if sheet_name in self.extents:
            return self.extents[sheet_name]
        return None
    
    # when a spreadsheet is added or deleted, update the extent of that sheet 
    def update_sheet_extent(self, sheet_name: str) -> None:
        if sheet_name in self.sheets:
            a = 0
            b = 0
            new_extent = (0,0)
            n = 0
            for i in self.sheets[sheet_name].keys():
                for j in range(len(i)):
                    if i[j].upper().isalpha():
                        a += ord(i[j].upper()) - 64 + (26 * n)
                    else:
                        b = int(i[j:]) 
                        break
                if (a,b) > new_extent:
                    new_extent = (a,b)
            self.extents[sheet_name] = new_extent
    
    # set the cell of the given location to the given contents
    # return true if successful, false otherwise
    def set_cell_contents(self, sheet_name: str, location: str, contents:str) -> bool:
        if sheet_name not in self.sheets:
            return False
        if not self.is_valid_location(location):
            return False
        # check if the sheet already has a cell, if not create one
        if location not in self.sheets[sheet_name]:
            self.sheets[sheet_name][location] = Cell(self.workbook, sheet_name, location, self.graph)
        # update the cell contents
        self.sheets[sheet_name][location].set_contents(contents)
        self.update_sheet_extent(sheet_name)
        return True

    # return the cell object at a particular location
    def get_cell(self, sheet_name: str, location: str) -> Cell:
        if sheet_name not in self.sheets:
            return False
        if not self.is_valid_location(location):
            return False
        # check if the sheet already has a cell, if not create one
        if location not in self.sheets[sheet_name]:
            self.sheets[sheet_name][location] = Cell(self.workbook, sheet_name, location, self.graph)
        return self.sheets[sheet_name][location]
    
    # return the contents of the cell at the given location
    def get_cell_contents(self, sheet_name: str, location: str):
        if sheet_name in self.sheets.keys():
            if location.upper() in self.sheets[sheet_name].keys():
                return self.sheets[sheet_name][location].get_contents()
        return None

    # return the value of the cell at the given location    
    def get_cell_value(self, sheet_name: str, location: str):
        if location.upper() in self.sheets[sheet_name].keys():
            return self.sheets[sheet_name][location].get_value()
        return None

    
