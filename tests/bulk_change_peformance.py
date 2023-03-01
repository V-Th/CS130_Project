# pylint: skip-file
import context
import string
import os
import cProfile, pstats, io
from sheets import *
from pstats import SortKey

def performance_run(workbook_cmd, name):
    pr = cProfile.Profile()
    pr.enable()

    # Code to run performance test on
    workbook_cmd()
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.CUMULATIVE, SortKey.TIME)
    ps.print_stats()
    print(name)
    print(s.getvalue())

def set_up():
    wb = Workbook()
    _, sheet1 = wb.new_sheet()
    _, _ = wb.new_sheet()
    for i in range(1, 1000):
        wb.set_cell_contents(sheet1, 'A'+str(i), '=A' + str(i+1))
    wb.set_cell_contents(sheet1, 'b1', '1')
    wb.set_cell_contents(sheet1, 'b2', 'Hello World!')
    wb.set_cell_contents(sheet1, 'b3', 'False')
    wb.set_cell_contents(sheet1, 'b4', '= a1')
    wb.set_cell_contents(sheet1, 'b5', '= sheet2!a1')
    wb.set_cell_contents(sheet1, 'b6', '= \"sheet2\"!a1')
    wb.set_cell_contents(sheet1, 'b7', '= IF(a1, a2, a3)')
    wb.set_cell_contents(sheet1, 'b8', '= $a1')
    wb.set_cell_contents(sheet1, 'b9', '= a$1')
    wb.set_cell_contents(sheet1, 'b10', '= $a$1')
    wb.set_cell_contents(sheet1, 'b11', '= b11')
    return sheet1, wb

def copy_sheet():
    sheet1, wb = set_up()

    exec = lambda : wb.copy_sheet(sheet1)
    performance_run(exec, "Copy Sheet")

def rename_sheet():
    sheet1, wb = set_up()

    exec = lambda : wb.rename_sheet(sheet1, "New Name")
    performance_run(exec, "Rename Sheet")

def copy_cells():
    sheet1, wb = set_up()
    exec = lambda : wb.copy_cells(sheet1, 'a1', 'b999', 'b1')
    performance_run(exec, "Copy Cells")

def move_cells():
    sheet1, wb = set_up()
    exec = lambda : wb.move_cells(sheet1, 'a1', 'b999', 'b1')
    performance_run(exec, "Move Cells")

def load_workbook():
    _, wb = set_up()
    file = open('wb.json', "x", encoding="utf-8")
    wb.save_workbook('wb.json')
    exec = lambda : Workbook.load_workbook('wb.json')
    file.close()
    performance_run(exec, "Load Workbook")
    if os.path.exists('wb.json'):
        os.remove('wb.json')


copy_sheet()
rename_sheet()
copy_cells()
move_cells()
load_workbook()
