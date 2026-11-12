import itertools as it
import random
import unittest
import sys
from collections import deque
from solutions import *
if "--student" in sys.argv:
    from student_week_06 import *

RNG=random.Random(20261031)
CASES=0

def equal(actual, expected):
    global CASES
    CASES += 1
    if actual != expected:
        raise AssertionError((actual, expected))

class Verification(unittest.TestCase):
    def test_topology(self):
        for n in range(1,5):
            for _ in range(80):
                edges=[[a,b] for a in range(n) for b in range(n) if a!=b and RNG.random()<.3]
                possible=any(all(order.index(b)<order.index(a) for a,b in edges) for order in it.permutations(range(n)))
                equal(can_finish(n,edges),possible)
                equal(acyclic_dfs_small(n,edges),possible)
                order=course_order(n,edges)
                if possible:
                    equal(sorted(order),list(range(n)))
                    equal(all(order.index(b)<order.index(a) for a,b in edges),True)
                else: equal(order,[])
        equal(can_finish(1,[[0,0]]),False)
        equal(len(course_order(2000,[[i+1,i] for i in range(1999)])),2000)

    def test_backtracking(self):
        for n in range(1,9):
            result=subsets(list(range(n)))
            equal({tuple(v) for v in result},{tuple(i for i in range(n) if mask>>i&1) for mask in range(1<<n)})
            equal(len({id(v) for v in result}),len(result))
        for candidates in ([2],[2,3],[2,3,5],[3,4,7]):
            for target in range(1,15):
                expected={tuple(value for value,count in zip(candidates,counts) for _ in range(count))
                          for counts in it.product(*(range(target//v+1) for v in candidates))
                          if sum(v*c for v,c in zip(candidates,counts))==target}
                equal({tuple(v) for v in combinations(candidates,target)},expected)

    def test_boundaries(self):
        equal(len(subsets(list(range(10)))),1024)
        equal(combinations([2],40),[[2]*20])
        equal(course_order(3,[]),[0,1,2])
        edges=[[1,0],[2,1]]; before=[r[:] for r in edges]; course_order(3,edges); equal(edges,before)


if __name__ == '__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Verification))
    print(f'Differential/boundary assertions: {CASES}; seed=20261031')
    raise SystemExit(not result.wasSuccessful())
