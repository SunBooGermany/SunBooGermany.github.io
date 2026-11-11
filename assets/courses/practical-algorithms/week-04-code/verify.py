"""Deterministic differential and boundary checks for Week 4."""
import random
import sys
from collections import deque
import solutions
import student_week_04
from structures import TreeNode, tree

impl = student_week_04 if '--student' in sys.argv else solutions
rng = random.Random(20261111)
checks = 0

def check(actual, expected):
    global checks
    assert actual == expected, (actual, expected)
    checks += 1

def snapshot(root):
    pending = [root] if root else []
    result = []
    while pending:
        node = pending.pop()
        result.append((id(node), node.val, id(node.left), id(node.right)))
        if node.right: pending.append(node.right)
        if node.left: pending.append(node.left)
    return result

def reference(root):
    levels = []
    def visit(node, depth):
        if node is None: return
        if depth == len(levels): levels.append([])
        levels[depth].append(node.val)
        visit(node.left, depth + 1)
        visit(node.right, depth + 1)
    visit(root, 0)
    return levels

def descendants(root):
    if root is None: return []
    return [root.val] + descendants(root.left) + descendants(root.right)

def reference_bst(root):
    if root is None: return True
    return (all(v < root.val for v in descendants(root.left))
            and all(v > root.val for v in descendants(root.right))
            and reference_bst(root.left) and reference_bst(root.right))

check(impl.max_depth(None), 0)
check(impl.level_order(None), [])
check(impl.valid_bst(tree([8, 3, 10, None, None, 6, 12])), False)
check(impl.valid_bst(tree([2, 2, 3])), False)
check(impl.valid_bst(tree([0, -(2**31), 2**31-1])), True)
check(impl.max_depth(tree([4, 2, 7, None, 3])), 3)
check(impl.level_order(tree([4, 2, 7, None, 3])), [[4], [2, 7], [3]])
for size in range(1, 40):
    for _ in range(12):
        root = TreeNode(rng.randrange(-20, 21))
        slots = [(root, 'left'), (root, 'right')]
        for i in range(size - 1):
            parent, side = slots.pop(rng.randrange(len(slots)))
            child = TreeNode(rng.randrange(-20, 21))
            setattr(parent, side, child)
            slots.extend([(child, 'left'), (child, 'right')])
        before = snapshot(root)
        levels = reference(root)
        check(impl.max_depth(root), len(levels))
        check(impl.level_order(root), levels)
        check(impl.valid_bst(root), reference_bst(root))
        check(snapshot(root), before)

for size in range(1, 45):
    values = rng.sample(range(1000), size)
    root = None
    for value in values:
        if root is None:
            root = TreeNode(value)
            continue
        node = root
        while True:
            side = 'left' if value < node.val else 'right'
            if getattr(node, side) is None:
                setattr(node, side, TreeNode(value)); break
            node = getattr(node, side)
    before = snapshot(root)
    check(impl.valid_bst(root), True)
    for k, expected in enumerate(sorted(values), 1):
        check(impl.kth_smallest(root, k), expected)
    check(snapshot(root), before)

# Official maximum-size cases avoid recursive test helpers.
root = TreeNode(0); node = root
for _ in range(9999):
    node.right = TreeNode(0); node = node.right
check(impl.max_depth(root), 10000)
root = TreeNode(0); node = root
for value in range(1, 10000):
    node.right = TreeNode(value); node = node.right
check(impl.valid_bst(root), True)
check(impl.kth_smallest(root, 10000), 9999)
node.val = -1
check(impl.valid_bst(root), False)
wide = [TreeNode(i % 1000) for i in range(2000)]
for i, node in enumerate(wide):
    if 2*i+1 < len(wide): node.left = wide[2*i+1]
    if 2*i+2 < len(wide): node.right = wide[2*i+2]
check(impl.level_order(wide[0]), reference(wide[0]))
print(f'{checks} checks passed; seed=20261111')
