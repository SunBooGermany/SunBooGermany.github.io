"""Executable Week 1 examples and traces. Run with Python 3.11+."""
import json
from solutions import two_sum, nearby_duplicate, two_sum_sorted, three_sum


def two_sum_brute(nums, target):
    for left in range(len(nums)):
        for right in range(left + 1, len(nums)):
            if nums[left] + nums[right] == target:
                return [left, right]
    return []


def nearby_brute(nums, k):
    return any(nums[i] == nums[j] and j - i <= k
               for i in range(len(nums)) for j in range(i + 1, len(nums)))


def two_sum_trace(nums, target):
    seen, trace = {}, []
    for index, value in enumerate(nums):
        needed = target - value
        trace.append(dict(index=index, value=value, needed=needed, seen=seen.copy()))
        if needed in seen:
            return trace, [seen[needed], index]
        seen[value] = index
    return trace, []


def nearby_trace(nums, k):
    latest, trace = {}, []
    for index, value in enumerate(nums):
        previous = latest.get(value)
        distance = None if previous is None else index - previous
        trace.append(dict(index=index, value=value, previous=previous, distance=distance))
        if previous is not None and distance <= k:
            return trace, True
        latest[value] = index
    return trace, False


def pointer_trace(numbers, target):
    left, right, trace = 0, len(numbers) - 1, []
    while left < right:
        total = numbers[left] + numbers[right]
        trace.append(dict(left=left, right=right, total=total))
        if total == target:
            return trace, [left + 1, right + 1]
        if total < target:
            left += 1
        else:
            right -= 1
    return trace, []


def verify_examples():
    first, answer = two_sum_trace([4, 8, 3], 7)
    assert answer == two_sum([4, 8, 3], 7) == [0, 2]
    assert first[-1]['seen'] == {4: 0, 8: 1}
    assert two_sum([3, 3], 6) == [0, 1]
    recent, found = nearby_trace([4, 7, 4, 4], 1)
    assert found == nearby_duplicate([4, 7, 4, 4], 1) is True
    assert recent[-1]['previous'] == 2 and recent[-1]['distance'] == 1
    assert nearby_duplicate([4, 7, 4, 4], 0) is False
    pointers, answer = pointer_trace([1, 4, 6, 9], 7)
    assert answer == two_sum_sorted([1, 4, 6, 9], 7) == [1, 3]
    assert [(row['left'],row['right'],row['total']) for row in pointers] == [(0,3,10),(0,2,7)]
    assert three_sum([-2, 0, 1, 1, 2]) == [[-2, 0, 2], [-2, 1, 1]]
    assert three_sum([0, 0, 0, 0]) == [[0, 0, 0]]
    assert three_sum([-2, -2, 0, 0, 2, 2]) == [[-2, 0, 2]]
    # Cross-check alternative algorithms, rather than their own line-by-line form.
    import itertools
    for size in range(1, 7):
        for values in itertools.product(range(3), repeat=size):
            for k in (0, 1, size):
                assert nearby_duplicate(values, k) == nearby_brute(values, k)
    assert 10000 * 9999 // 2 == 49995000
    return dict(two_sum=first, nearby_duplicate=recent, sorted_pair=pointers)


if __name__ == '__main__':
    print(json.dumps(verify_examples(), indent=2))
    print('Week 1 examples, traces, and small-input baseline comparisons: passed')
