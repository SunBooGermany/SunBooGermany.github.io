"""Week 6 implementation workspace.

Run python verify.py --student after completing the tasks.
Use python trace_lab.py --case FUNCTION --student to inspect states.
실습: 문제별 작은 예제를 예측한 뒤 구현하고 상태 변화를 비교합니다.
"""
from collections import deque
import heapq

def can_finish(n, prerequisites):
    """Build prerequisite→course edges and incoming counts. Only zero-indegree vertices enter the queue. This cycle has no initial ready course; processed count stays zero. Remove [0,2] to make all three processable.

    선수과목→다음 과목 방향으로 간선과 진입차수를 만듭니다. 진입차수가 0인 정점만 queue에 넣습니다. 이 순환은 처음부터 준비된 과목이 없어 처리 개수가 0입니다. [0,2]를 빼면 세 과목을 모두 처리할 수 있습니다.
    Example: can_finish(3, [[1, 0], [2, 1], [0, 2]]) => False
    """
    raise NotImplementedError("Implement the exercise")

def course_order(n, prerequisites):
    """Append each ready course to the order before reducing its successors’ indegrees. Course 3 becomes ready only after both 1 and 2. Validate every edge using positions; [0,2,1,3] is also valid.

    준비된 과목을 순서에 넣고 다음 과목들의 진입차수를 줄입니다. 3은 1과 2를 모두 끝낸 뒤 준비됩니다. 각 간선의 앞뒤 위치를 검사하세요. [0,2,1,3]도 유효합니다.
    Example: course_order(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) => [0, 1, 2, 3]
    """
    raise NotImplementedError("Implement the exercise")

def subsets(nums):
    """At each search node, save a copy of path. Choose an element, recurse on later positions, then pop it. Saving path itself aliases one changing list. With n=2, there are four outputs including the empty subset.

    탐색 노드마다 path의 복사본을 저장합니다. 원소 선택, 뒤쪽 위치 재귀, pop 순서로 진행합니다. path 자체를 저장하면 하나의 변하는 list를 공유합니다. n=2의 출력은 빈 부분집합을 포함해 네 개입니다.
    Example: subsets([1, 2],) => [[], [1], [1, 2], [2]]
    """
    raise NotImplementedError("Implement the exercise")

def combinations(candidates, target):
    """Track remaining target and the first allowed candidate index. Reuse the chosen index to permit repeats, but never return to smaller indices. Stop at remaining=0. Explain why [3,2,2] is not a second answer.

    남은 target과 선택 가능한 첫 인덱스를 둡니다. 반복 사용을 위해 같은 인덱스로 재귀하되 더 작은 인덱스로 돌아가지 않습니다. 나머지가 0이면 저장합니다. [3,2,2]가 별도 답이 아닌 이유를 설명하세요.
    Example: combinations([2, 3, 6, 7], 7) => [[2, 2, 3], [7]]
    """
    raise NotImplementedError("Implement the exercise")
