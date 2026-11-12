import itertools as it
import random
import unittest
import sys
from collections import deque
from solutions import *
if "--student" in sys.argv:
    from student_week_07 import *

RNG=random.Random(20261031)
CASES=0

def equal(actual, expected):
    global CASES
    CASES += 1
    if actual != expected:
        raise AssertionError((actual, expected))

def brute_coin(coins, amount):
    queue, seen = deque([(0,0)]), {0}
    while queue:
        value, count = queue.popleft()
        if value == amount:
            return count
        for coin in coins:
            nxt = value + coin
            if nxt <= amount and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt,count+1))
    return -1

class Verification(unittest.TestCase):
    def test_dp(self):
        for _ in range(250):
            values=[RNG.randrange(8) for _ in range(RNG.randrange(1,10))]
            expected=max(sum(v for i,v in enumerate(values) if mask>>i&1) for mask in range(1<<len(values)) if not mask & (mask<<1))
            equal(rob(values),expected)
        for coins in ([1],[2],[1,3,4],[2,5],[3,7]):
            for amount in range(35): equal(coin_change(coins,amount),brute_coin(coins,amount))
        import math
        for rows in range(1,9):
            for cols in range(1,9): equal(unique_paths(rows,cols),math.comb(rows+cols-2,rows-1))
        for _ in range(140):
            a=''.join(RNG.choices('abc',k=RNG.randrange(1,8)))
            b=''.join(RNG.choices('abc',k=RNG.randrange(1,8)))
            subsequences=lambda text:{''.join(text[i] for i in range(len(text)) if mask>>i&1) for mask in range(1<<len(text))}
            equal(lcs(a,b),max(map(len,subsequences(a)&subsequences(b))))

    def test_boundaries(self):
        equal(rob([400]*100),20000)
        equal(coin_change([1],10000),10000)
        equal(lcs('a'*1000,'a'*1000),1000)
        equal(unique_paths(1,100),1)
        equal(coin_change([2147483647],1),-1)
        values=[3,1,4,2]; rob(values); equal(values,[3,1,4,2])


if __name__ == '__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Verification))
    print(f'Differential/boundary assertions: {CASES}; seed=20261031')
    raise SystemExit(not result.wasSuccessful())
