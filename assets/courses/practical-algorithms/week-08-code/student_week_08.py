"""Week 8 implementation workspace.

Run python verify.py --student after completing the tasks.
Use python trace_lab.py --case FUNCTION --student to inspect states.
실습: 문제별 작은 예제를 예측한 뒤 구현하고 상태 변화를 비교합니다.
"""
from collections import deque
import heapq

def can_jump(nums):
    """Maintain the farthest reachable index. Only positions at or below that boundary can extend it. The boundary stays at 3, so index 4 cannot supply a jump. Change the zero to 1 and explain the difference.

    도달 가능한 가장 먼 인덱스를 유지합니다. 그 경계 안에 있는 위치만 경계를 늘릴 수 있습니다. 경계가 3에 멈추므로 인덱스 4의 점프는 사용할 수 없습니다. 0을 1로 바꾸고 결과 차이를 설명하세요.
    Example: can_jump([3, 2, 1, 0, 4],) => False
    """
    raise NotImplementedError("Implement the exercise")

def min_jumps(nums):
    """Track the end reachable with the current jump count and the farthest endpoint found within it. Increment jumps only when the current interval ends. Intervals end at 0,2,4; two jumps reach the last index.

    현재 점프 횟수로 갈 수 있는 끝과 그 구간에서 새로 찾은 가장 먼 끝을 둡니다. 현재 구간을 다 읽을 때만 점프 수를 늘립니다. 구간 끝은 0,2,4가 되므로 두 번이면 마지막에 도착합니다.
    Example: min_jumps([2, 3, 1, 1, 4],) => 2
    """
    raise NotImplementedError("Implement the exercise")

def gas_start(gas, cost):
    """Accumulate total surplus and the balance since the current start. A negative segment balance discards every start in that segment. Surpluses are -2,-2,-2,3,3; restart at 3, then verify one full circular lap.

    전체 잉여량과 현재 출발점 이후 잔량을 누적합니다. 구간 잔량이 음수면 그 구간의 모든 출발점을 버립니다. 잉여량은 -2,-2,-2,3,3이므로 3에서 다시 시작한 뒤 한 바퀴의 잔량을 확인하세요.
    Example: gas_start([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) => 3
    """
    raise NotImplementedError("Implement the exercise")

def islands(grid):
    """Choose connected-component search rather than a greedy frontier. Draw the region (0,0),(0,1),(1,1) and the separate cell (2,2). Explain why diagonal contact is not an edge, then test an all-water grid.

    greedy 경계 대신 연결 요소 탐색을 선택합니다. (0,0),(0,1),(1,1) 영역과 별개인 (2,2)를 그립니다. 대각선 접촉이 간선이 아닌 이유를 설명하고 모두 물인 격자도 검사하세요.
    Example: islands([list('110'), list('010'), list('001')],) => 2
    """
    raise NotImplementedError("Implement the exercise")


def weighted_jobs(jobs):
    """Maximum reward from nonoverlapping jobs; touching endpoints are allowed.

    Sort by end; dp[i] is the best reward from the first i jobs.
    Compare skipping with reward + the last compatible prefix optimum.
    끝 시각으로 정렬하고 건너뛰기와 호환 구간에 보상 더하기를 비교합니다.
    Example: [[0,2,4],[2,3,3],[1,4,8]] => 8. Preserve the input.
    """
    raise NotImplementedError("Implement the job-selection exercise")
