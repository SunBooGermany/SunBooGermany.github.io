from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val, self.left, self.right = val, left, right


def tree(values):
    """Level-order representation; None marks an absent child."""
    if not values or values[0] is None:
        return None
    root = TreeNode(values[0])
    queue, items = deque([root]), iter(values[1:])
    for parent in iter(queue.popleft, None):
        for side in ("left", "right"):
            value = next(items, None)
            if value is not None:
                child = TreeNode(value)
                setattr(parent, side, child)
                queue.append(child)
        if not queue:
            break
    return root
