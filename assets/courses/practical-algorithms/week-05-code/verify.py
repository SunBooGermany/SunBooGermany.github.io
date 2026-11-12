import itertools as it
import random
import unittest
import sys
from collections import deque
from solutions import *
if "--student" in sys.argv:
    from student_week_05 import *

RNG=random.Random(20261031)
CASES=0

def equal(actual, expected):
    global CASES
    CASES += 1
    if actual != expected:
        raise AssertionError((actual, expected))

def brute_islands(grid):
    land = {(r,c) for r,row in enumerate(grid) for c,v in enumerate(row) if v == '1'}
    count = 0
    while land:
        group = {land.pop()}
        while True:
            added = {p for p in land if any(abs(p[0]-q[0])+abs(p[1]-q[1]) == 1 for q in group)}
            if not added:
                break
            land -= added
            group |= added
        count += 1
    return count

def brute_rot(grid):
    board = [row[:] for row in grid]
    minutes = 0
    while True:
        fresh = {(r,c) for r,row in enumerate(board) for c,v in enumerate(row) if v == 1}
        if not fresh:
            return minutes
        changed = {(r,c) for r,c in fresh if any(
            0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] == 2
            for nr,nc in ((r-1,c),(r+1,c),(r,c-1),(r,c+1)))}
        if not changed:
            return -1
        for r,c in changed:
            board[r][c] = 2
        minutes += 1

class Verification(unittest.TestCase):
    def test_heap_intervals(self):
        for _ in range(250):
            values=[RNG.randrange(-5,6) for _ in range(RNG.randrange(1,20))]
            for k in (1,len(values),(len(values)+1)//2):
                equal(kth_largest(values,k),sorted(values,reverse=True)[k-1])
            intervals=[]
            for _ in range(RNG.randrange(1,8)):
                a,b=sorted(RNG.choices(range(8),k=2)); intervals.append([a,b])
            result=merge_intervals(intervals)
            # Half-integer probes cover every possible endpoint and interior here.
            probes=[value/2 for value in range(15)]
            for point in probes:
                equal(any(a<=point<=b for a,b in result),any(a<=point<=b for a,b in intervals))
            equal(all(a[1]<b[0] for a,b in zip(result,result[1:])),True)

    def test_grids(self):
        for bits in it.product('01',repeat=6):
            grid=[list(bits[:3]),list(bits[3:])]
            equal(islands(grid),brute_islands(grid))
        for values in it.product(range(3),repeat=6):
            grid=[list(values[:3]),list(values[3:])]
            equal(rot_minutes(grid),brute_rot(grid))

    def test_boundaries(self):
        equal(kth_largest(list(range(100000)),50000),50000)
        equal(islands([['1']*300 for _ in range(300)]),1)
        equal(rot_minutes([[2]+[1]*9]+[[1]*10 for _ in range(9)]),18)
        for fn,arg in [(merge_intervals,[[1,8],[2,3]]),(islands,[['1','0'],['0','1']]),(rot_minutes,[[2,1],[1,1]])]:
            before=[r[:] for r in arg]; fn(arg); equal(arg,before)


if __name__ == '__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Verification))
    print(f'Differential/boundary assertions: {CASES}; seed=20261031')
    raise SystemExit(not result.wasSuccessful())
