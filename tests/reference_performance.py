import context
import string
import cProfile, pstats, io
from sheets import *
from pstats import SortKey

def chain_refs():
    pr = cProfile.Profile()
    pr.enable()

    # Code to run performance test on
    wb = Workbook()
    _, name = wb.new_sheet()

    for i in range(1, 100):
        wb.set_cell_contents(name, 'A'+str(i), '=A' + str(i+1))
    wb.set_cell_contents(name, 'A100', '10')
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.TIME, SortKey.CUMULATIVE)
    ps.print_stats('sheets')
    print("Long reference chain")
    print(s.getvalue())

def one_ref_for_all():
    pr = cProfile.Profile()
    pr.enable()

    # Code to run performance test on
    wb = Workbook()
    _, name = wb.new_sheet()

    for i in range(1, 100):
        wb.set_cell_contents(name, 'A'+str(i), '=A100')
    wb.set_cell_contents(name, 'A100', '10')
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.TIME, SortKey.CUMULATIVE)
    ps.print_stats("sheets")
    print("Several short references")
    print(s.getvalue())

def long_loop():
    pr = cProfile.Profile()
    pr.enable()

    # Code to run performance test on
    wb = Workbook()
    _, name = wb.new_sheet()

    for i in range(1, 100):
        wb.set_cell_contents(name, 'A'+str(i), '=A' + str(i+1))
    wb.set_cell_contents(name, 'A100', '=A1')
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.TIME, SortKey.CUMULATIVE)
    ps.print_stats("sheets")
    print("Long loop test")
    print(s.getvalue())

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
multi_loops()
make_one_break_one()
make_all_break_all()