import context
import cProfile, pstats, io
from sheets import *
from pstats import SortKey

def break_recursion_limit():
    wb = Workbook()
    _, name = wb.new_sheet()
    for i in range(1, 2000):
        wb.set_cell_contents(name, 'A'+str(i), '=A' + str(i+1))

    pr = cProfile.Profile()
    pr.enable()

    # Code to run performance test on
    wb.set_cell_contents(name, 'A2000', '=A1')
    
    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats(SortKey.TIME, SortKey.CUMULATIVE)
    ps.print_stats("sheets")
    print("Break Recursion")
    print(s.getvalue())

break_recursion_limit()