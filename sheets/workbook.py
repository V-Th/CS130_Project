#!/usr/bin/env python3
from .cell import _Cell
from .cellerror import *
from .cellgraph import _CellGraph
import re
import lark
import string
import logging
import json

_RE = re.compile('[A-Za-z]+[1-9][0-9]*')
_SHEET_CHARS = set(" .?!,:;!@#$%^&*()-_"+string.ascii_letters+string.digits)
    
class Workbook():
    def __init__(self):
        self.workbook = self
        self._sheets = {}
        self._extents = {}
        self._display_sheets = {}
        self._missing_sheets = {}
        self._graph = _CellGraph()
        self.on_cells_changed = None
        self.changed_cells = []

    def save_workbook(self, f: string):
        if (f[-5:] != '.json'):
            raise ValueError
        sheet_list = []
        for sheet in self.list_sheets():
            sheet_dict = {'name':sheet, 'cell_contents':{}}
            for loc in self._sheets[sheet.upper()]:
                sheet_dict['cell_contents'][loc] = self._sheets[sheet.upper()][loc].toJSON()
            sheet_list.append(sheet_dict)
        out_file = open(f, "w")
        json.dump({'sheets':sheet_list}, out_file, indent = 4)
        out_file.close()
    
    def load_workbook(self, f: string):
        try:
            f = open(f)
            data = json.load(f)
        except:
            raise ValueError
        for sheet in data['sheets']:
            _, name = self.new_sheet(sheet['name'])
            for loc in sheet['cell_contents']:
                self.set_cell_contents(name, loc, sheet['cell_contents'][loc][1:-1])
        f.close()

    def _call_notification(self):
        if self.on_cells_changed is not None and len(self.changed_cells) != 0: 
            self.on_cells_changed(self, self.changed_cells)
        self.changed_cells.clear()
    
    def notify_cells_changed(self, on_cells_changed):
        self.on_cells_changed = on_cells_changed

    def num_sheets(self) -> int:
        return len(self._sheets)

    def list_sheets(self) -> list[str]:
        return [name for name in self._display_sheets.values()]
    
    def _sheet_name_exists(self, sheet_name: str) -> bool:
        return sheet_name.upper() in self._sheets.keys()
    
    def _location_exists(self, sheet_name:str, loc: str) -> bool:
        return loc.upper() in self._sheets[sheet_name.upper()].keys()
    
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
        if _RE.match(location) is None:
            return False
        # check that location is within limits A-ZZZZ and 1-9999
        a, b = self._loc_to_tuple(location)
        if a > 475254 or b > 9999:
            return False
        return True

    # Check missing sheets to update cells that may need it
    def _check_missing_sheets(self, sheet_name: str):
        if sheet_name.upper() in self._missing_sheets.keys():
            for cell in self._missing_sheets[sheet_name.upper()]:
                old_val = cell.get_value()
                cell.update_value()
                if (old_val == cell.get_value()):
                    continue
                self.changed_cells.append((cell.sheet_name[0:], cell.location[0:]))
            self._update_references(self._missing_sheets[sheet_name.upper()])
            self._call_notification()
    
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
        self._update_sheet_extent(sheet_name.upper(), None)
        self._check_missing_sheets(sheet_name)
        return (self.num_sheets()-1, sheet_name)

    def _update_references(self, cells: list):
        original_set = cells.copy()
        ref_cells = []
        self._graph.dfs_nodes(cells, ref_cells)
        for cell in ref_cells:
            old_val = cell.get_value()
            cell.update_value()
            if (old_val == cell.get_value()):
                continue
            if cell in original_set:
                continue
            self.changed_cells.append((cell.sheet_name[0:], cell.location[0:]))

    # delete the given spreadsheet
    # Take cells of deleted sheet and updates them to None
    # This triggers the update_value for cells relying on them
    def del_sheet(self, sheet_name: str) -> None:
        if self._sheet_name_exists(sheet_name):
            dead_sheet = self._sheets.pop(sheet_name.upper())
            self._display_sheets.pop(sheet_name.upper())
            self._extents.pop(sheet_name.upper())
            self._update_references(list(dead_sheet.values()))
            self._call_notification()
        else:
            raise KeyError

    # return number of rows and columns in the given spreadsheet
    def get_sheet_extent(self, sheet_name: str) -> tuple[int, int]:
        if self._sheet_name_exists(sheet_name):
            return self._extents[sheet_name.upper()]
        else:
            raise KeyError
    
    # when a spreadsheet is added or deleted, update the extent of that sheet 
    def _update_sheet_extent(self, sheet_name: str, cell: _Cell) -> None:
        if not self._sheet_name_exists(sheet_name):
            return
        max_a, max_b = 0, 0
        if cell is None:
            self._extents[sheet_name.upper()] = (max_a, max_b)
            return
        if cell.get_contents() is None:
            for loc in self._sheets[sheet_name.upper()].keys():
                content = self._sheets[sheet_name.upper()][loc.upper()].get_contents()
                if content is None:
                    continue
                a, b = self._loc_to_tuple(loc)
                if a > max_a:
                    max_a = a
                if b > max_b:
                    max_b = b
        elif cell.get_contents():
            a, b = self._loc_to_tuple(cell.location)
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
                        node.value = CellError(CellErrorType.CIRCULAR_REFERENCE, "Circular reference detected")
                continue
            for i in set:
                cell_sheet = i.sheet_name.upper()
                cell_loc = i.location.upper()
                cell_err = CellError(CellErrorType.CIRCULAR_REFERENCE, "Circular reference detected")
                self._sheets[cell_sheet][cell_loc].value = cell_err
        return

    # Internal call to add cells to sheet
    def _set_cell_contents(self, sheet_name: str, loc: str, contents:str):
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_location(loc):
            raise ValueError

        # check if the sheet already has a cell, if not create one
        if not self._location_exists(sheet_name, loc):
            self._sheets[sheet_name.upper()][loc.upper()] = _Cell(self.workbook, sheet_name, loc)
        else:
            self._graph.remove_node(self._sheets[sheet_name.upper()][loc.upper()])
            for f_sheet in self._missing_sheets.keys():
                cells = self._missing_sheets[f_sheet]
                if self._sheets[sheet_name.upper()][loc.upper()] in cells:
                    cells.remove(self._sheets[sheet_name.upper()][loc.upper()])

        # update the cell contents
        old_val = self._sheets[sheet_name.upper()][loc.upper()].get_value()
        self._sheets[sheet_name.upper()][loc.upper()].set_contents(contents)
        self._sheets[sheet_name.upper()][loc.upper()].update_value()
        if (old_val != self._sheets[sheet_name.upper()][loc.upper()].get_value()):
            self.changed_cells.append((sheet_name, loc))
    
    # set the cell of the given location to the given contents
    # return true if successful, false otherwise
    def set_cell_contents(self, sheet_name: str, loc: str, contents:str) -> None:
        self._set_cell_contents(sheet_name, loc, contents)
        self._check_for_loop()
        self._update_references([self._sheets[sheet_name.upper()][loc.upper()]])
        self._call_notification()
        self._update_sheet_extent(sheet_name.upper(), self._sheets[sheet_name.upper()][loc.upper()])

    # return the cell object at a particular location
    def add_dependency(self, src_cell: _Cell, location: str, sheet_name: str) -> None:
        if not self._sheet_name_exists(sheet_name):
            if sheet_name.upper() not in self._missing_sheets.keys():
                self._missing_sheets[sheet_name.upper()] = []
            self._missing_sheets[sheet_name.upper()].append(src_cell)
            assert self._sheet_name_exists(sheet_name)
        assert self._is_valid_location(location.upper())

        # check if the sheet already has a cell, if not create one
        if not self._location_exists(sheet_name, location):
            self._sheets[sheet_name.upper()][location.upper()] = _Cell(self.workbook, sheet_name, location)
        dest_cell = self._sheets[sheet_name.upper()][location.upper()]
        self._graph.add_edge(src_cell, dest_cell)
    
    # return the contents of the cell at the given location
    def get_cell_contents(self, sheet_name: str, location: str):
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_location(location):
            raise ValueError
        if not self._location_exists(sheet_name, location):
            return None
        return self._sheets[sheet_name.upper()][location.upper()].get_contents()

    # return the value of the cell at the given location    
    def get_cell_value(self, sheet_name: str, location: str):
        # parameter validation
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_location(location):
            raise ValueError
        if not self._location_exists(sheet_name, location):
            return None
        return self._sheets[sheet_name.upper()][location.upper()].get_value()

    def rename_sheet(self, sheet_name: str, new_name: str):
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_sheet(new_name):
            raise ValueError

        # Replace sheet name in all dictionaries in the workbook
        self._display_sheets.pop(sheet_name.upper())
        self._display_sheets[new_name.upper()] = new_name
        extent = self._extents.pop(sheet_name.upper())
        self._extents[new_name.upper()] = extent
        loc_cells = self._sheets.pop(sheet_name.upper())
        self._sheets[new_name.upper()] = {}

        # Change the sheet name value within the cells of the sheet
        while loc_cells:
            loc, cell = loc_cells.popitem()
            cell.sheet_name = new_name
            self._sheets[new_name.upper()][loc.upper()] = cell

        # Change the sheet name references in formulas
        cells = list(self._sheets[new_name.upper()].values())
        direct_refs = self._graph.direct_refs(cells)
        new_ref = new_name
        if ' ' in new_name:
            new_ref = "\'"+new_name+"\'"
        for cell in direct_refs:
            cell.rename_sheet(new_ref, sheet_name)
        self._check_missing_sheets(new_name)
    
    def move_sheet(self, sheet_name: str, index: int):
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if index >= self.num_sheets():
            raise IndexError
        sheets = list(self._display_sheets.items())
        entry = (sheet_name.upper(), self._display_sheets[sheet_name.upper()])
        sheets.remove(entry)
        sheets.insert(index, entry)
        self._display_sheets = dict(sheets)

    def copy_sheet(self, sheet_name: str):
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        sheet = self._sheets[sheet_name.upper()]
        copy_name = self._display_sheets[sheet_name.upper()]
        n = 1
        while (self._sheet_name_exists(copy_name + "_" + str(n))):
            n += 1
        copy_name = copy_name + '_' + str(n)
        idx, copy_name = self.new_sheet(copy_name)
        for loc, cell in sheet.items():
            self._set_cell_contents(copy_name, loc, cell.get_contents())
        self._call_notification()
        self._check_missing_sheets(copy_name)
        return idx, copy_name