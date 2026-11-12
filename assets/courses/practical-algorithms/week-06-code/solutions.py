from collections import deque
import heapq


def can_finish(n, prerequisites):
    return len(course_order(n, prerequisites)) == n


def course_order(n, prerequisites):
    graph, indegree = [[] for _ in range(n)], [0] * n
    for after, before in prerequisites:
        graph[before].append(after)
        indegree[after] += 1
    queue = deque(v for v in range(n) if indegree[v] == 0)
    order = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)
    return order if len(order) == n else []


def subsets(nums):
    result, path = [], []

    def visit(start):
        result.append(path.copy())
        for index in range(start, len(nums)):
            path.append(nums[index])
            visit(index + 1)
            path.pop()

    visit(0)
    return result


def combinations(candidates, target):
    values, result, path = sorted(candidates), [], []

    def visit(start, remaining):
        if remaining == 0:
            result.append(path.copy())
            return
        for index in range(start, len(values)):
            value = values[index]
            if value > remaining:
                break
            path.append(value)
            visit(index, remaining - value)
            path.pop()

    visit(0, target)
    return result


def acyclic_dfs_small(n, prerequisites):
    """Comparison demonstration; use Kahn's algorithm for long chains."""
    graph, state = [[] for _ in range(n)], [0] * n
    for after, before in prerequisites:
        graph[before].append(after)

    def visit(node):
        if state[node] == 1:
            return False
        if state[node] == 2:
            return True
        state[node] = 1
        for neighbor in graph[node]:
            if not visit(neighbor):
                return False
        state[node] = 2
        return True

    return all(visit(node) for node in range(n))
