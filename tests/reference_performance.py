import context
import string
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
    ps.print_stats('sheets')
    print(name)
    print(s.getvalue())

def chain_refs():
    # Set up
    wb = Workbook()
    _, name = wb.new_sheet()
    for i in range(1, 300):
        wb.set_cell_contents(name, 'A'+str(i), '=A' + str(i+1))

    # Code to run performance test on
    exec = lambda : wb.set_cell_contents(name, 'A300', '10')
    performance_run(exec, "Long Chain Update")

def one_ref_for_all():
    # Set Up
    wb = Workbook()
    _, name = wb.new_sheet()
    for i in range(1, 100):
        wb.set_cell_contents(name, 'A'+str(i), '=A100')

    # Code to run performance test on
    exec = lambda : wb.set_cell_contents(name, 'A100', '10')
    performance_run(exec, "Several Short Updates")

def long_loop():
    # Set Up
    wb = Workbook()
    _, name = wb.new_sheet()
    for i in range(1, 300):
        wb.set_cell_contents(name, 'A'+str(i), '=A' + str(i+1))

    # Code to run performance test on
    exec = lambda : wb.set_cell_contents(name, 'A300', '=A1')
    performance_run(exec, "Long Chain Cycle")

def m_by_n_update():
    # Set up
    wb = Workbook()
    _, name = wb.new_sheet()
    for j in range(10):
        char = string.ascii_uppercase[j]
        for i in range(1, 30):
            wb.set_cell_contents(name, char+str(i), '='+char+str(i+1))
        wb.set_cell_contents(name, char+'30', '='+string.ascii_uppercase[j+1]+'1')

    # Code to run performance test on
    exec = lambda : wb.set_cell_contents(name, 'J30', '10')
    performance_run(exec, "M by N Update")

def m_by_n_cycle():
    # Set up
    wb = Workbook()
    _, name = wb.new_sheet()
    for j in range(10):
        char = string.ascii_uppercase[j]
        for i in range(1, 30):
            wb.set_cell_contents(name, char+str(i), '='+char+ str(i+1))
        wb.set_cell_contents(name, char+'30', '='+string.ascii_uppercase[j+1]+'1')

    # Code to run performance test on
    exec = lambda : wb.set_cell_contents(name, 'J30', '=A1')
    performance_run(exec, "M by N Cycle")

def multi_loops():
    pr = cProfile.Profile()
    pr.enable()

    # Code to run performance test on
    wb = Workbook()
    _, name = wb.new_sheet()

    for letter in string.ascii_lowercase:
        for i in range(1, 6):
            wb.set_cell_contents(name, letter+str(i), '='+letter+str(i+1))
        wb.set_cell_contents(name, letter+'6', '='+letter+'1')
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.TIME, SortKey.CUMULATIVE)
    ps.print_stats("sheets")
    print("Multiple loops test")
    print(s.getvalue())

def make_one_break_one():
    pr = cProfile.Profile()
    pr.enable()

    # Code to run performance test on
    wb = Workbook()
    _, name = wb.new_sheet()

    for letter in string.ascii_lowercase:
        for i in range(1, 6):
            wb.set_cell_contents(name, letter+str(i), '='+letter+str(i+1))
        wb.set_cell_contents(name, letter+'6', '='+letter+'1')
        wb.set_cell_contents(name, letter+'6', '1')
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.TIME, SortKey.CUMULATIVE)
    ps.print_stats("sheets")
    print("Make one break one test")
    print(s.getvalue())

def make_all_break_all():
    pr = cProfile.Profile()
    pr.enable()

    # Code to run performance test on
    wb = Workbook()
    _, name = wb.new_sheet()

    for letter in string.ascii_lowercase:
        for i in range(1, 6):
            wb.set_cell_contents(name, letter+str(i), '='+letter+str(i+1))
        wb.set_cell_contents(name, letter+'6', '='+letter+'1')
    for letter in string.ascii_lowercase:
        wb.set_cell_contents(name, letter+'6', '1')
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.TIME, SortKey.CUMULATIVE)
    ps.print_stats("sheets")
    print("Make all break all test")
    print(s.getvalue())

chain_refs()
one_ref_for_all()
long_loop()
m_by_n_update()
m_by_n_cycle()
# multi_loops()
# make_one_break_one()
# make_all_break_all()