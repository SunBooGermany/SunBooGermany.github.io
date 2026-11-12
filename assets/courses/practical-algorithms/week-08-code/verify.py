import itertools as it
import random
import unittest
import sys
from collections import deque
from solutions import *
from assessment_reference import weighted_jobs
if "--student" in sys.argv:
    from student_week_08 import *

RNG=random.Random(20261031)
CASES=0

def equal(actual, expected):
    global CASES
    CASES += 1
    if actual != expected:
        raise AssertionError((actual, expected))

def brute_jump(nums):
    distance = [float('inf')] * len(nums)
    distance[0] = 0
    for i,value in enumerate(nums):
        for j in range(i+1,min(len(nums),i+value+1)):
            distance[j] = min(distance[j],distance[i]+1)
    return distance[-1]

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

def brute_jobs(jobs):
    best = 0
    for mask in range(1 << len(jobs)):
        selected = sorted((job for i,job in enumerate(jobs) if mask >> i & 1))
        if all(a[1] <= b[0] for a,b in zip(selected,selected[1:])):
            best = max(best,sum(job[2] for job in selected))
    return best

class Verification(unittest.TestCase):
    def test_greedy(self):
        for n in range(1,7):
            for values in it.product(range(3),repeat=n):
                expected=brute_jump(values)
                equal(can_jump(values),expected<float('inf'))
                if expected<float('inf'): equal(min_jumps(values),expected)
        for _ in range(450):
            n=RNG.randrange(1,8)
            gas=[RNG.randrange(5) for _ in range(n)]
            cost=[RNG.randrange(5) for _ in range(n)]
            possible=[]
            for start in range(n):
                tank=0
                for offset in range(n):
                    i=(start+offset)%n; tank+=gas[i]-cost[i]
                    if tank<0: break
                else: possible.append(start)
            result=gas_start(gas,cost)
            equal(result in possible if possible else result==-1,True)
        equal(gas_start([5,0,4],[6,1,2]),2)

    def test_assessment_and_islands(self):
        for bits in it.product('01',repeat=6):
            grid=[list(bits[:3]),list(bits[3:])]
            before=[r[:] for r in grid]
            equal(islands(grid),brute_islands(grid)); equal(grid,before)
        for _ in range(150):
            jobs=[]
            for _ in range(RNG.randrange(1,9)):
                start=RNG.randrange(10); end=RNG.randrange(start+1,12)
                jobs.append([start,end,RNG.randrange(10)])
            before=[job[:] for job in jobs]
            equal(weighted_jobs(jobs),brute_jobs(jobs)); equal(jobs,before)


    def test_boundaries(self):
        equal(can_jump([1]*10000),True)
        equal(min_jumps([1]*10000),9999)
        equal(gas_start([0]*99999+[1],[0]*99998+[1,0]),99999)
        equal(islands([['1']*300 for _ in range(300)]),1)
        equal(weighted_jobs([[0,2,3],[2,4,3],[0,4,10]]),10)


if __name__ == '__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Verification))
    print(f'Differential/boundary assertions: {CASES}; seed=20261031')
    raise SystemExit(not result.wasSuccessful())
