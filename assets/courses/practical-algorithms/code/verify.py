"""Verify the published Week 1 package against independent small-input baselines."""
import itertools
import random
from solutions import two_sum, nearby_duplicate, two_sum_sorted, three_sum
from week01_walkthrough import verify_examples


def run():
    verify_examples()
    rng=random.Random(20261031)
    count=0
    for _ in range(500):
        values=[rng.randrange(-4,5) for _ in range(rng.randrange(3,9))]
        expected={tuple(sorted(t)) for t in itertools.combinations(values,3) if sum(t)==0}
        actual=three_sum(values)
        assert {tuple(t) for t in actual}==expected
        assert len(actual)==len(expected)
        target=rng.randrange(-8,9)
        pairs=[(i,j) for i in range(len(values)) for j in range(i+1,len(values)) if values[i]+values[j]==target]
        if len(pairs)==1:
            assert tuple(two_sum(values,target))==pairs[0]
            ordered=sorted(values)
            left,right=two_sum_sorted(ordered,target)
            assert left<right and ordered[left-1]+ordered[right-1]==target
        k=rng.randrange(len(values)+1)
        assert nearby_duplicate(values,k)==any(values[i]==values[j] and j-i<=k for i in range(len(values)) for j in range(i+1,len(values)))
        count+=1
    print(f'Week 1 traces and {count} mixed baseline comparisons passed; seed=20261031')


if __name__=='__main__':
    run()
