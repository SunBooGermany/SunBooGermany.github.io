import itertools
import sys
import student_week_03 as student
import solutions
from structures import linked, linked_values

impl = student if '--student' in sys.argv else solutions
checks = 0
for rows in range(1, 5):
    for cols in range(1, 5):
        values = list(range(rows * cols))
        matrix = [values[i:i+cols] for i in range(0, len(values), cols)]
        for target in range(-1, len(values)+1):
            assert impl.search_matrix(matrix, target) == (target in values)
            checks += 1
for n in range(1, 10):
    values = list(range(0, 2*n, 2))
    for k in range(n):
        rotated = values[k:] + values[:k]
        for target in range(-1, 2*n+1):
            expected = rotated.index(target) if target in rotated else -1
            assert impl.search_rotated(rotated, target) == expected
            checks += 1
def nodes(head):
    out, seen = [], set()
    while head:
        assert head not in seen, 'cycle'
        seen.add(head); out.append(head); head = head.next
    return out
for n in range(6):
    for values in itertools.product(range(2), repeat=n):
        head = linked(values); original = nodes(head)
        result = impl.reverse_list(head)
        assert nodes(result) == original[::-1]
        checks += 1
lists = [list(c) for n in range(5) for c in itertools.combinations_with_replacement(range(3), n)]
for a in lists:
    for b in lists:
        x, y = linked(a), linked(b)
        before = nodes(x) + nodes(y)
        result = impl.merge_lists(x, y)
        after = nodes(result)
        assert [n.val for n in after] == sorted(a+b)
        assert len(after) == len(before) and set(after) == set(before)
        checks += 1
print(f'{checks} checks passed')
