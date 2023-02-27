'''
The workbook module implements the Workbook class that fits the specified
API requirements. Furthermore, it implements internal calls for use with
the cell and cellgraph modules.
'''
import re
import os
import json
import string
import logging
from typing import Optional
from .cell import _Cell
from .cellgraph import _CellGraph
from .cellerror import CellErrorType, CellError

_RE = re.compile('[$]?[A-Za-z]+[$]?[1-9][0-9]*')
_SHEET_CHARS = set(" .?!,:;!@#$%^&*()-_"+string.ascii_letters+string.digits)

class Workbook():
    '''
    A workbook containing zero or more named spreadsheets.

    Any and all operations on a workbook that may affect calculated cell values
    should cause the workbook's contents to be updated properly.
    '''

    def __init__(self):
        self.workbook = self
        self.sheets = {}
        self._extents = {}
        self._display_sheets = {}
        #self._display_sheets = [None]
        self._missing_sheets = {}
        self._graph = _CellGraph()
        self.on_cells_changed = []
        self.changed_cells = []

    def save_workbook(self, filename: string):
        '''
        Instance method to save a workbook to a text file or file-like object
        in JSON format.

        If an IO write error occurs, let any raised exception propagaet through
        '''
        if not filename.endswith('.json'):
            raise ValueError
        sheet_list = []
        for sheet in self.list_sheets():
            sheet_dict = {'name':sheet, 'cell_contents':{}}
            for loc in self.sheets[sheet.upper()]:
                sheet_dict['cell_contents'][loc] = self.sheets[sheet.upper()][loc].toJSON()
            sheet_list.append(sheet_dict)
        with open(filename, encoding="utf-8") as out_file:
            contents = out_file.write()
            if self.num_sheets() > 0:
                json.dump({'sheets':sheet_list}, contents, indent = 4)

    def load_workbook(self, filename: string):
        '''
        This is a static method to load a workbook from a test file or
        file-like object in JSON format, and return the new Workbook
        instance.

        If the contents of the input cannot be parsed by the Python json
        module then a json.JSONDecodeError should be raised by the method.
        '''
        if os.path.getsize(filename) == 0:
            return
        file = open(filename, "r", encoding="utf-8")
        data = json.load(file)
        for sheet in data['sheets']:
            _, name = self.new_sheet(sheet['name'])
            for loc in sheet['cell_contents']:
                self.set_cell_contents(name, loc, sheet['cell_contents'][loc][1:-1])
        file.close()

    def _call_notification(self):
        # Runs through all given notification functions and calls them on the
        # cells
        for call_func in self.on_cells_changed:
            try:
                call_func(self, self.changed_cells)
            # A general exception is used to catch any exception that a
            # notification may throw
            # pylint: disable=W0703
            except Exception:
                continue
        self.changed_cells.clear()

    def notify_cells_changed(self, notify_function):
        '''
        Requaest that all changes to cell values in the workbook are reported
        to the sepcified notify_function. The values passed to the notify
        function are the workbook, and an iterable of 2-tuples of strings,
        of the form ([sheet name], [cell location]). The notify_function is
        expected not to reutnr any value; any reutnr-value will be ignored.
        '''
        self.on_cells_changed.append(notify_function)

    def num_sheets(self) -> int:
        '''
        Reports the number of sheets in the workbook.
        '''
        return len(self.sheets)

    def list_sheets(self) -> list[str]:
        '''
        Returns a list of sheets that does not manipulation the internal list
        of sheets.
        '''
        return [name for name in self._display_sheets.values()]

    def _sheet_name_exists(self, sheet_name: str) -> bool:
        # Checks that the sheet name exists within the workbook
        return sheet_name.upper() in self.sheets

    def _location_exists(self, sheet_name:str, loc: str) -> bool:
        # Checks that the location exists in the sheet
        return loc.upper() in self.sheets[sheet_name.upper()].keys()

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
        if sheet_name.strip() != sheet_name:
            logging.info("Workbook: is_valid_sheet: leading or trailing whitespace")
            return False
        if not set(sheet_name).issubset(_SHEET_CHARS):
            logging.info("Workbook: is_valid_sheet: illegal charcter in sheet name")
            return False
        return True

    def loc_to_tuple(self, loc: str):
        '''
        Converts a location to 2-tuple (row, col)
        '''
        row, col = 0, 0
        for i, char in enumerate(loc):
            if char.upper().isalpha():
                row = (row * 26) + (ord(char.upper()) - ord('A') + 1)
            else:
                col = int(loc[i:])
                break
        return (row, col)

    def tuple_to_loc(self, row: int, col: int) -> str:
        '''
        Converts row and col to location in workbook
        '''
        letter_str = ""
        while row > 0:
            modulo = (row - 1) % 26
            letter_str = (chr((modulo) + ord('A'))) + letter_str
            row = (row - 1) // 26
        if not self._is_valid_location(letter_str + str(col)):
            return "#REF!"
        return letter_str + str(col)

    # returns whether the given string represents a valid location in the sheet
    def _is_valid_location(self, location: str) -> bool:
        if len(location) > 8 or len(location) < 2:
            return False
        if _RE.match(location) is None:
            return False
        # check that location is within limits A-ZZZZ and 1-9999
        row, col = self.loc_to_tuple(location)
        if row > 475254 or col > 9999:
            return False
        return True

    def _check_missing_sheets(self, sheet_name: str):
        '''
        Check missing sheets to update cells that may need it
        '''
        sheet_upper = sheet_name.upper()
        if not sheet_upper in self._missing_sheets:
            return
        for cell in self._missing_sheets[sheet_upper]:
            old_val = cell.get_value()
            cell.update_dependencies()
            cell.update_value()
            if old_val == cell.get_value():
                continue
            self.changed_cells.append((cell.sheet_name, cell.location))
        self._update_references(self._missing_sheets[sheet_upper])
        self._call_notification()

    def new_sheet(self, sheet_name: str = None) -> tuple[int, str]:
        '''
        Creates new empty spreadsheet if the given sheet_name is valid
        returns the index and name of the new spreadsheet
        '''
        if sheet_name is None:
            num = 1
            while(self._sheet_name_exists("Sheet" + str(num))):
                num += 1
            sheet_name = "Sheet" + str(num)
        elif not self._is_valid_sheet(sheet_name):
            raise ValueError
        self.sheets[sheet_name.upper()] = {}
        self._display_sheets[sheet_name.upper()] = sheet_name
        self._update_sheet_extent(sheet_name.upper(), None)
        self._check_missing_sheets(sheet_name)
        return (self.num_sheets()-1, sheet_name)

    # Takes a list of cells who have been updated and updates their references
    # Does NOT UPDATE the given cells
    def _update_references(self, cells: list):
        original_set = cells.copy()
        ref_cells = []
        self._graph.bfs_nodes(cells, ref_cells)
        for cell in ref_cells:
            if cell in original_set:
                continue
            old_val = cell.get_value()
            cell.update_value()
            if old_val == cell.get_value():
                continue
            self.changed_cells.append((cell.sheet_name, cell.location))

    def _update_cells_in_loop(self, cell, sccs: set[_Cell]):
        cells_to_update = []
        for in_loop in sccs:
            old_val = in_loop.get_value()
            detail = "Circular reference detected"
            in_loop.value = CellError(CellErrorType(2), detail)
            if old_val != in_loop.get_value():
                sheet_name = in_loop.sheet_name
                loc = in_loop.location
                self.changed_cells.append((sheet_name, loc))
            for child in self._graph.get_children(in_loop) - sccs:
                if child in cells_to_update:
                    continue
                cells_to_update.append(child)
        self._update_cell_values(cell, cells_to_update, sccs)

    def _update_cell_values(self, cell, cells_to_update: list[_Cell], sccs: set):
        dynamic_refs = self._graph.dynamic_refs()
        while cells_to_update:
            to_update = cells_to_update.pop(0)
            old_val = to_update.get_value()
            to_update.update_value()
            if self._graph.has_dynamic_refs(to_update):
                dynamic_refs = self._graph.dynamic_refs()
                sccs = self._graph.particular_SCC(cell)
                if to_update in sccs:
                    self._update_cells_in_loop(to_update, sccs)
            if old_val != to_update.get_value():
                sheet_name = to_update.sheet_name
                loc = to_update.location
                self.changed_cells.append((sheet_name, loc))
            for child in self._graph.get_children(to_update):
                if child in cells_to_update:
                    continue
                if child in sccs - dynamic_refs:
                    continue
                cells_to_update.append(child)
                for g_child in self._graph.get_children(child):
                    if g_child in cells_to_update:
                        cells_to_update.remove(g_child)
                        cells_to_update.append(g_child)

    # Update given cell and all cells dependent on given cell
    def _update_cell(self, cell: _Cell):
        # Search for SCC's involved with given cell
        sccs = self._graph.particular_SCC(cell)
        # If the cell is in a SCC, then all cells touching it must be CIRCREF
        if cell in sccs:
            self._update_cells_in_loop(cell, sccs)
        else:
            self._update_cell_values(cell, [cell], sccs)

    def del_sheet(self, sheet_name: str) -> None:
        '''
        Delete the given spreadsheet
        Take cells of the deleted sheet and updates them to None
        '''
        if self._sheet_name_exists(sheet_name):
            sheet_upper = sheet_name.upper()
            dead_sheet = self.sheets.pop(sheet_upper)
            self._display_sheets.pop(sheet_upper)
            self._extents.pop(sheet_upper)
            self._update_references(list(dead_sheet.values()))
            self._call_notification()
        else:
            raise KeyError

    def get_sheet_extent(self, sheet_name: str) -> tuple[int, int]:
        '''
        Return number of rows and columns in the given spreadsheet
        '''
        if self._sheet_name_exists(sheet_name):
            return self._extents[sheet_name.upper()]
        raise KeyError

    def _search_for_extent(self, sheet_upper: str):
        max_a, max_b = 0, 0
        for loc in self.sheets[sheet_upper].keys():
            content = self.sheets[sheet_upper][loc.upper()].get_contents()
            if content is None:
                continue
            row, col = self.loc_to_tuple(loc)
            if row > max_a:
                max_a = row
            if col > max_b:
                max_b = col
        return (max_a, max_b)

    # when a spreadsheet is added or deleted, update the extent of that sheet
    def _update_sheet_extent(self, sheet_name: str, cell: _Cell) -> None:
        sheet_upper = sheet_name.upper()
        if not self._sheet_name_exists(sheet_name):
            return
        if cell is None:
            max_a, max_b = self._search_for_extent(sheet_upper)
        elif cell.get_contents() is None:
            if self.loc_to_tuple(cell.location) != self._extents[sheet_upper]:
                return
            max_a, max_b = self._search_for_extent(sheet_upper)
        elif cell.get_contents():
            max_a, max_b = self._extents[sheet_upper]
            row, col = self.loc_to_tuple(cell.location)
            if row > max_a:
                max_a = row
            if col > max_b:
                max_b = col
        self._extents[sheet_upper] = (max_a, max_b)

    # Update the cellgraph and check for loops
    def _check_for_loop(self):
        self._graph.lazy_SCC()
        # for those in SCC sets with other, set CIRCREF error
        cells_in_loop = []
        for cell in self._graph.nodes:
            if cell in self._graph.sccs:
                old_value = cell.value
                cells_in_loop.append(cell)
                err_str = "Circular reference detected"
                cell.value = CellError(CellErrorType(2), err_str)
                if old_value != cell.value:
                    self.changed_cells.append((cell.sheet_name, cell.location))
        return cells_in_loop

    # Internal call to add cells to sheet, avoids unnecessary checks
    def _set_cell_contents(self, sheet_name: str, loc: str, contents:str):
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_location(loc):
            raise ValueError

        # check if the sheet already has a cell, if not create one
        sheet_upper = sheet_name.upper()
        if not self._location_exists(sheet_name, loc):
            self.sheets[sheet_upper][loc.upper()] = _Cell(self.workbook, sheet_name, loc)
        else:
            self._graph.remove_node(self.sheets[sheet_upper][loc.upper()])
            for _, cells in self._missing_sheets.items():
                if self.sheets[sheet_upper][loc.upper()] in cells:
                    cells.remove(self.sheets[sheet_upper][loc.upper()])

        # old_val = self.sheets[sheet_upper][loc.upper()].get_value()
        self.sheets[sheet_upper][loc.upper()].set_contents(contents)
        # self.sheets[sheet_upper][loc.upper()].update_value()
        # if old_val != self.sheets[sheet_upper][loc.upper()].get_value():
        #     self.changed_cells.append((sheet_name, loc))

    # set the cell of the given location to the given contents
    def set_cell_contents(self, sheet_name: str, loc: str, contents:str) -> None:
        '''
        Set the cell of the given location to the given contents
        '''
        self._set_cell_contents(sheet_name, loc, contents)
        cell = self.sheets[sheet_name.upper()][loc.upper()]
        # self._update_refs_w_dynamic_refs(cell)
        # cells_updated = [cell]
        # cells_updated.extend(self._check_for_loop())
        # self._update_references(cells_updated)
        self._update_cell(cell)
        self._call_notification()
        self._update_sheet_extent(sheet_name.upper(), cell)

    def find_dest_cell(self, src_cell: _Cell, loc: str, sheet_name: str):
        '''
        Find the destination cell that the src_cell is trying to reference
        Store in missing sheet if the sheet does not yet exist
        '''
        sheet_upper = sheet_name.upper()
        if not self._sheet_name_exists(sheet_name):
            if sheet_upper not in self._missing_sheets:
                self._missing_sheets[sheet_upper] = []
            self._missing_sheets[sheet_upper].append(src_cell)
            return None
        if not self._is_valid_location(loc.upper()):
            return None

        # check if the sheet already has a cell, if not create one
        if not self._location_exists(sheet_name, loc):
            blank_cell = _Cell(self.workbook, sheet_name, loc)
            self.sheets[sheet_upper][loc.upper()] = blank_cell
        return self.sheets[sheet_upper][loc.upper()]

    def add_dependency(self, src_cell: _Cell, loc: str, sheet_name: str) -> None:
        '''
        Add dependency between cells in graph
        '''
        dest_cell = self.find_dest_cell(src_cell, loc, sheet_name)
        if dest_cell is None:
            return
        self._graph.add_edge(src_cell, dest_cell)

    def clear_dynamic(self, src_cell: _Cell):
        '''
        Clear the dynamic dependencies of a cell before evaluating
        '''
        self._graph.clear_dynamic_dep(src_cell)

    def add_dynamic_dep(self, src_cell: _Cell, loc: str, sheet_name: str):
        '''
        Add dynamic dependency between cells in graph
        '''
        dest_cell = self.find_dest_cell(src_cell, loc, sheet_name)
        if dest_cell is None:
            return
        self._graph.add_dynamic_dep(src_cell, dest_cell)

    # return the contents of the cell at the given location
    def get_cell_contents(self, sheet_name: str, loc: str):
        '''
        Return the contents of the cell at the given location.
        '''
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_location(loc):
            raise ValueError
        if not self._location_exists(sheet_name, loc):
            return None
        return self.sheets[sheet_name.upper()][loc.upper()].get_contents()

    # return the value of the cell at the given location
    def get_cell_value(self, sheet_name: str, location: str):
        '''
        Return the value of the cell at the given location
        '''
        # parameter validation
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_location(location):
            raise ValueError
        if not self._location_exists(sheet_name, location):
            return None
        return self.sheets[sheet_name.upper()][location.upper()].get_value()

    def rename_sheet(self, sheet_name: str, new_name: str):
        '''
        Rename the specified sheet to the new sheet name. Additionally, all
        cell formulas that referenced the original sheet name are updated to
        reference the new sheet name.

        If the sheet_name is not found, a KeyError is raised.

        If the new_sheet_name is an empty string or is otherwise invalid, a
        ValueError is raised.
        '''
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._is_valid_sheet(new_name):
            raise ValueError

        # Replace sheet name in all dictionaries in the workbook
        self._display_sheets.pop(sheet_name.upper())
        self._display_sheets[new_name.upper()] = new_name
        extent = self._extents.pop(sheet_name.upper())
        self._extents[new_name.upper()] = extent
        loc_cells = self.sheets.pop(sheet_name.upper())
        self.sheets[new_name.upper()] = {}

        # Change the sheet name value within the cells of the sheet
        while loc_cells:
            loc, cell = loc_cells.popitem()
            cell.sheet_name = new_name
            self.sheets[new_name.upper()][loc.upper()] = cell

        # Change the sheet name references in formulas
        cells = list(self.sheets[new_name.upper()].values())
        direct_refs = self._graph.direct_refs(cells)
        new_ref = new_name
        if ' ' in new_name:
            new_ref = "\'"+new_name+"\'"
        for cell in direct_refs:
            cell.rename_sheet(new_ref, sheet_name)
        self._check_missing_sheets(new_name)

    def move_sheet(self, sheet_name: str, index: int):
        '''
        Move the specified sheet to the specified index in the workbook's
        ordered sequence of sheets. The index is 0-index and has a max of
        workbook.num_sheets() - 1.
        '''
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
        '''
        Make a copy of the specified sheet, storing the copy at the end of the
        workbook's sequence of sheets. The copy's name is generated by
        appending "_1", "_2", ... to the original sheet's name.
        '''
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        sheet = self.sheets[sheet_name.upper()]
        copy_name = self._display_sheets[sheet_name.upper()]
        num = 1
        while (self._sheet_name_exists(copy_name + "_" + str(num))):
            num += 1
        copy_name = copy_name + '_' + str(num)
        idx, copy_name = self.new_sheet(copy_name)
        for loc, cell in sheet.items():
            self._set_cell_contents(copy_name, loc, cell.get_contents())
            self._update_cell(self.sheets[copy_name.upper()][loc.upper()])
        self._call_notification()
        self._update_sheet_extent(copy_name.upper(), None)
        self._check_missing_sheets(copy_name)
        return idx, copy_name

    def _check_relative_location(self, sheet_name: str, start_location: str,
            end_location: str, to_location: str, to_sheet):
        if not self._sheet_name_exists(sheet_name):
            raise KeyError
        if not self._location_exists(sheet_name, start_location):
            raise KeyError
        if not self._location_exists(sheet_name, end_location):
            raise KeyError
        if to_sheet is not None and not self._sheet_name_exists(to_sheet):
            raise ValueError
        if not self._is_valid_location(to_location):
            raise ValueError

    def _get_relative_contents(self, x_1, x_2, y_1, y_2, x_diff, y_diff, sheet_name, to_sheet, move: bool):
        contents = {}
        for i in range(min(x_1, x_2), max(x_1, x_2) + 1):
            for j in range(min(y_1, y_2), max(y_1, y_2) + 1):
                old_location = self.tuple_to_loc(i, j)
                start_cell = self.sheets[sheet_name.upper()][old_location.upper()]
                contents[old_location] = start_cell.get_relative_contents(x_diff, y_diff, to_sheet)
                if move:
                    self.set_cell_contents(sheet_name, old_location, None)
        return contents

    def _copy_move_cells(self, sheet_name: str, start_location: str,
            end_location: str, to_location: str, move, to_sheet: Optional[str] = None):
        if to_sheet is None:
            to_sheet = sheet_name

        self._check_relative_location(sheet_name, start_location, end_location,
            to_location, to_sheet)

        min_location = min(start_location, end_location)
        x_diff = self.loc_to_tuple(to_location)[0] - self.loc_to_tuple(min_location)[0]
        y_diff = self.loc_to_tuple(to_location)[1] - self.loc_to_tuple(min_location)[1]

        x_1, y_1 = self.loc_to_tuple(start_location)
        x_2, y_2 = self.loc_to_tuple(end_location)

        contents = self._get_relative_contents(x_1, x_2, y_1, y_2, x_diff, y_diff,
            sheet_name, to_sheet, move)

        for i in range(min(x_1, x_2), max(x_1, x_2) + 1):
            for j in range(min(y_1, y_2), max(y_1, y_2) + 1):
                old_location = self.tuple_to_loc(i, j)
                new_location = self.tuple_to_loc(i + x_diff, j + y_diff)
                self.set_cell_contents(to_sheet, new_location, contents[old_location])

    def move_cells(self, sheet_name: str, start_location: str,
            end_location: str, to_location: str, to_sheet: Optional[str] = None):
        '''
        Move cells from one location to another, possibly moving them to
        another sheet. All formulas in the area being moved will also have all
        relative and mixed cell-references updated by the relative distance
        each formula is being copied.
        '''
        self._copy_move_cells(sheet_name, start_location, end_location, 
                              to_location, True, to_sheet)

    def copy_cells(self, sheet_name: str, start_location: str,
            end_location: str, to_location: str, to_sheet: Optional[str] = None):
        '''
        Copy cells from one location to another, possibly moving them to
        another sheet. All formulas in the area being moved will also have all
        relative and mixed cell-references updated by the relative distance
        each formula is being copied.
        '''
        self._copy_move_cells(sheet_name, start_location, end_location, 
                              to_location, False, to_sheet)