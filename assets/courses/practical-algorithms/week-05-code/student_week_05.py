"""Week 5 implementation workspace.

Run python verify.py --student after completing the tasks.
Use python trace_lab.py --case FUNCTION --student to inspect states.
실습: 문제별 작은 예제를 예측한 뒤 구현하고 상태 변화를 비교합니다.
"""
from collections import deque
import heapq

def kth_largest(nums, k):
    """Keep a min-heap of the largest k values seen so far. Replace its root only with a larger value. The root is the smallest retained value, hence the kth largest overall. Try k=1 and duplicates.

    지금까지 본 큰 값 k개를 min-heap에 보관합니다. 루트보다 큰 값만 루트를 대체합니다. 루트는 보관한 값 중 가장 작으므로 전체에서 k번째 큰 값입니다. k=1과 중복 값도 확인하세요.
    Example: kth_largest([3, 2, 1, 5, 6, 4], 2) => 5
    """
    raise NotImplementedError("Implement the exercise")

def merge_intervals(intervals):
    """Sort by start. Compare each interval with the last merged end; extend with max(end, next_end) on overlap. Test [1,6] with [2,3] so the end never shrinks.

    시작점으로 정렬합니다. 다음 구간을 마지막 병합 구간의 끝과 비교하고 겹치면 max(끝, 다음 끝)으로 늘립니다. [1,6]과 [2,3]으로 끝이 줄어들지 않는지 검사하세요.
    Example: merge_intervals([[1, 3], [2, 6], [8, 10]],) => [[1, 6], [8, 10]]
    """
    raise NotImplementedError("Implement the exercise")

def islands(grid):
    """Scan cells. On unseen land, increment the component count and flood-fill its four-neighbor region. Mark when scheduling a cell to avoid duplicate work. Diagonally touching land remains separate.

    칸을 훑다가 방문하지 않은 땅이면 개수를 늘리고 상하좌우 연결 영역을 방문합니다. 탐색 대상으로 넣을 때 표시하면 중복 처리를 막습니다. 대각선으로 닿은 땅은 별개입니다.
    Example: islands([list('110'), list('010'), list('001')],) => 2
    """
    raise NotImplementedError("Implement the exercise")

def rot_minutes(grid):
    """Put all initially rotten cells in one queue. Process a whole level per minute and decrease fresh on each newly rotten cell. The fresh counts are 6→4→2→1→0. Try an isolated fresh cell: return -1.

    처음 썩은 칸을 모두 한 queue에 넣습니다. 한 깊이를 1분으로 처리하고 새로 썩을 때 fresh를 줄입니다. 남은 개수는 6→4→2→1→0입니다. 고립된 신선한 칸이 있으면 -1인지 확인하세요.
    Example: rot_minutes([[2, 1, 1], [1, 1, 0], [0, 1, 1]],) => 4
    """
    raise NotImplementedError("Implement the exercise")
